import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("vector_store")

class VectorStore:
    def __init__(self):
        self.index_path = settings.faiss_index_path
        self.model_name = settings.embedding_model
        self.model = SentenceTransformer(self.model_name)

        self.dim = self.model.get_sentence_embedding_dimension()
        self.index_file = os.path.join(self.index_path, "index.faiss")
        self.text_file = os.path.join(self.index_path, "texts.npy")

        os.makedirs(self.index_path, exist_ok=True)

        if os.path.exists(self.index_file):
            logger.info("loading_faiss_index")
            self.index = faiss.read_index(self.index_file)
            self.texts = list(np.load(self.text_file, allow_pickle=True))
        else:
            logger.info("creating_new_faiss_index")
            self.index = faiss.IndexFlatL2(self.dim)
            self.texts = []

    def add_documents(self, documents: list[str]):
        embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        self.index.add(embeddings)
        self.texts.extend(documents)

        faiss.write_index(self.index, self.index_file)
        np.save(self.text_file, np.array(self.texts, dtype=object))

    def search(self, query: str, top_k: int = 5):
        if self.index.ntotal == 0:
            return []

        query_emb = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        _, indices = self.index.search(query_emb, top_k)
        return [self.texts[i] for i in indices[0] if i < len(self.texts)]

    def health(self):
        return {"faiss_vectors": self.index.ntotal}

vector_store = VectorStore()
