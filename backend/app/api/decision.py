from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.agents.graph import build_decision_graph
from app.retrieval.vector_store import VectorStore

router = APIRouter(prefix="/decision", tags=["decision"])


class DecisionRequest(BaseModel):
    query: str = Field(..., min_length=5)


class DecisionResponse(BaseModel):
    decision: Optional[str]
    confidence: float
    analysis: Optional[str]
    verification_notes: Optional[str]
    evidence: List[str]


@router.post("/", response_model=DecisionResponse)
async def make_decision(payload: DecisionRequest):
    """
    Executes the full multi-agent financial decision workflow.
    """

    # 1️⃣ Retrieve evidence
    vector_store = VectorStore()
    evidence = vector_store.similarity_search(payload.query, k=5)

    # 2️⃣ Initialize LangGraph state as DICT (IMPORTANT)
    state: Dict[str, Any] = {
        "query": payload.query,
        "evidence": evidence,
        "applicable_policies": [],
        "analysis": None,
        "verified": False,
        "verification_notes": None,
        "decision": None,
        "confidence": 0.0,
    }

    # 3️⃣ Run LangGraph workflow
    graph = build_decision_graph()
    final_state: Dict[str, Any] = await graph.ainvoke(state)

    # 4️⃣ Return structured response
    return {
        "decision": final_state.get("decision"),
        "confidence": final_state.get("confidence", 0.0),
        "analysis": final_state.get("analysis"),
        "verification_notes": final_state.get("verification_notes"),
        "evidence": final_state.get("evidence", []),
    }
