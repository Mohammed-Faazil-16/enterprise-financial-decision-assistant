from pathlib import Path
from typing import List

import faiss
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class VectorStore:
    def __init__(self) -> None:
        self.index_path = Path(settings.faiss_index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)

        self.model = SentenceTransformer(settings.embedding_model)
        self.dim = self.model.get_sentence_embedding_dimension()

        self.index_file = self.index_path / "index.faiss"
        self.text_file = self.index_path / "documents.txt"

        if self.index_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            self.documents = self.text_file.read_text(encoding="utf-8").splitlines()
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.documents = []

    def add_documents(self, docs: List[str]) -> None:
        embeddings = self.model.encode(docs, convert_to_numpy=True)
        self.index.add(embeddings)
        self.documents.extend(docs)

        faiss.write_index(self.index, str(self.index_file))
        self.text_file.write_text(
            "\n".join(self.documents), encoding="utf-8"
        )

    def similarity_search(self, query: str, k: int = 5) -> List[str]:
        embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(embedding, k)

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results
