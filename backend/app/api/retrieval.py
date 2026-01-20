from fastapi import APIRouter
from pydantic import BaseModel
from app.retrieval.service import retrieve_top_k

router = APIRouter()

class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/")
async def retrieve(payload: RetrievalRequest):
    results = await retrieve_top_k(payload.query, payload.top_k)
    return {
        "query": payload.query,
        "results": results,
    }
