import uuid
import json
import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.decision import Decision
from app.db.audit_events import log_event
from app.decision.engine import decision_engine
from app.core.logging import logger

router = APIRouter()


@router.post("/decision")
def make_decision(payload: dict, db: Session = Depends(get_db)):
    try:
        request_id = str(uuid.uuid4())

        input_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

        log_event(db, None, "DECISION_REQUESTED", {"request_id": request_id})

        result = decision_engine.run(payload)

        decision_row = Decision(
            request_id=request_id,
            input_hash=input_hash,
            input_payload=payload,

            decision=result["decision"],
            confidence=result["confidence"],
            conditions=result.get("conditions"),

            evidence=result["evidence"],
            reasoning_summary=result["analysis"],
            verification_notes=result.get("verification_notes"),

            model_provider="ollama",
            model_name=result.get("model", "unknown"),
            model_version=None,

            system_version="local-v1",
        )

        db.add(decision_row)
        db.flush()

        log_event(
            db,
            decision_row.id,
            "DECISION_PERSISTED",
            {"confidence": result["confidence"]},
        )

        db.commit()
        return result

    except Exception as e:
        db.rollback()
        logger.exception("Decision transaction failed")
        raise HTTPException(status_code=500, detail="Decision failed")
