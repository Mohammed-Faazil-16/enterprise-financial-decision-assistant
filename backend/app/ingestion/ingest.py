from typing import List
from app.retrieval.vector_store import VectorStore
from app.core.logging import get_logger

logger = get_logger()


class DocumentIngestor:
    def __init__(self) -> None:
        self.vector_store = VectorStore()

    async def ingest_documents(self, documents: List[str]) -> None:
        if not documents:
            logger.warning("ingestion_skipped", reason="no_documents")
            return

        self.vector_store.add_documents(documents)

        logger.info(
            "documents_ingested",
            document_count=len(documents),
        )
