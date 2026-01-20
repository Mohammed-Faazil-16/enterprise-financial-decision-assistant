from typing import List
from app.retrieval.vector_store import vector_store
from app.core.logging import get_logger

logger = get_logger("ingestion")

class DocumentIngestor:
    async def ingest_documents(self, documents: List[str]):
        if not documents:
            return

        vector_store.add_documents(documents)
        logger.info(f"documents_embedded count={len(documents)}")
