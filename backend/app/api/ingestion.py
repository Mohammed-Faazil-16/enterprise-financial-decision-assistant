from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
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
    # 1️⃣ Store in Postgres
    async with AsyncSessionLocal() as session:
        stmt = insert(TextSource).values(
            source=payload.source,
            text=payload.text
        )
        await session.execute(stmt)
        await session.commit()

    # 2️⃣ Store in FAISS
    await ingestor.ingest_documents([payload.text])

    return {"status": "stored_and_embedded"}
