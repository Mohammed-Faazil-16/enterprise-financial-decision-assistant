from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class DecisionRequest(BaseModel):
    query: str

@router.post("/")
async def make_decision(payload: DecisionRequest):
    return {
        "query": payload.query,
        "decision": "This is a placeholder financial decision response"
    }
