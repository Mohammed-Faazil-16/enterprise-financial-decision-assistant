from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db.session import AsyncSessionLocal
from app.db.models.text_source import TextSource

router = APIRouter()

class IngestRequest(BaseModel):
    source: str
    text: str

@router.post("/")
async def ingest(payload: IngestRequest):
    async with AsyncSessionLocal() as session:
        stmt = insert(TextSource).values(
            source=payload.source,
            text=payload.text
        )
        await session.execute(stmt)
        await session.commit()

    return {"status": "stored"}
