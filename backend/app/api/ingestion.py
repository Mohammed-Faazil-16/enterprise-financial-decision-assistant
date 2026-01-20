from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import insert
from app.db.session import AsyncSessionLocal
from app.db.models.text_source import TextSource
from app.ingestion.ingest import DocumentIngestor

router = APIRouter()
ingestor = DocumentIngestor()

class IngestRequest(BaseModel):
    source: str
    text: str

@router.post("/")
async def ingest(payload: IngestRequest):
    async with AsyncSessionLocal() as session:
        await session.execute(
            insert(TextSource).values(
                source=payload.source,
                text=payload.text
            )
        )
        await session.commit()

    await ingestor.ingest_documents([payload.text])
    return {"status": "stored_and_embedded"}
