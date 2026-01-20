from app.retrieval.vector_store import vector_store

async def retrieve_top_k(query: str, top_k: int = 3):
    return vector_store.search(query, top_k)
