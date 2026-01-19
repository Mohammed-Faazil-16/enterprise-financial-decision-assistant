from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def ingest():
    return {"status": "ingestion placeholder"}
