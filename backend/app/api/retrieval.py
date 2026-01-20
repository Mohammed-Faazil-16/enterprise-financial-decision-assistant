from fastapi import APIRouter
from pydantic import BaseModel
from app.retrieval.vector_store import vector_store

router = APIRouter()


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/")
async def retrieve(payload: RetrievalRequest):
    results = vector_store.search(payload.query, payload.top_k)
    return {
        "query": payload.query,
        "results": results,
    }
