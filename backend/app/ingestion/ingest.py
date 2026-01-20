from typing import List
from app.retrieval.vector_store import vector_store
from app.core.logging import get_logger

logger = get_logger("ingestion")


class DocumentIngestor:
    def __init__(self) -> None:
        self.vector_store = vector_store

    async def ingest_documents(self, documents: List[str]) -> None:
        if not documents:
            logger.warning("ingestion_skipped", reason="no_documents")
            return

        self.vector_store.add_documents(documents)

        logger.info(
            "documents_ingested_and_embedded",
            document_count=len(documents),
        )
