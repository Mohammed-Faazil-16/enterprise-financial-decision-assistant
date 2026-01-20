from fastapi import APIRouter
from pydantic import BaseModel
from app.decision.engine import decision_engine

router = APIRouter()

class DecisionRequest(BaseModel):
    query: str

@router.post("/")
async def make_decision(payload: DecisionRequest):
    result = await decision_engine.decide(payload.query)
    return result
