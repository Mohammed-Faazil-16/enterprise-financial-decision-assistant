from app.vector.faiss_store import faiss_store

async def retrieve_top_k(query: str, top_k: int = 3) -> list[str]:
    results = faiss_store.search(query, top_k=top_k)
    return [r["text"] for r in results]
