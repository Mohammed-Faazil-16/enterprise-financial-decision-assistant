from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

from app.ingestion.ingest import DocumentIngestor

router = APIRouter(prefix="/ingest", tags=["ingestion"])


class TextIngestRequest(BaseModel):
    documents: List[str] = Field(..., min_items=1)


class IngestResponse(BaseModel):
    status: str
    document_count: int


@router.post("/text", response_model=IngestResponse)
async def ingest_text(payload: TextIngestRequest):
    ingestor = DocumentIngestor()
    await ingestor.ingest_documents(payload.documents)

    return {
        "status": "ingested",
        "document_count": len(payload.documents),
    }
