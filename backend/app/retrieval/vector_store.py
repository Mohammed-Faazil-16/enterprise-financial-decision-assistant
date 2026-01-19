"""
Vector Store placeholder.
Later this will be replaced by FAISS / Chroma / PGVector.
"""

class VectorStore:
    def __init__(self):
        self.ready = True

    def health(self):
        return "vector store ready"


# GLOBAL INSTANCE (this is what engine.py imports)
vector_store = VectorStore()
