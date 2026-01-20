from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db.models.decision import Decision
from app.db.models.audit_log import AuditLog

async def persist_decision(session: AsyncSession, payload: dict):
    decision_stmt = insert(Decision).values(
        query=payload.get("query"),
        decision=payload.get("decision"),
        confidence=payload.get("confidence"),
    ).returning(Decision.id)

    result = await session.execute(decision_stmt)
    decision_id = result.scalar()

    audit_stmt = insert(AuditLog).values(
        event_type="decision_created",
        payload={
            "decision_id": decision_id,
            "decision": payload,
        },
    )

    await session.execute(audit_stmt)
    await session.commit()

    return decision_id
