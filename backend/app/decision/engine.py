from app.retrieval.vector_store import vector_store
from app.agents.graph import build_decision_graph
from app.db.session import AsyncSessionLocal
from app.decision.persist import persist_decision

class DecisionEngine:
    def __init__(self):
        self.vector_store = vector_store
        self.graph = build_decision_graph()

    async def decide(self, query: str) -> dict:
        evidence = self.vector_store.search(query, top_k=5)

        state = {
            "query": query,
            "evidence": evidence,
        }

        result = await self.graph.ainvoke(state)

        async with AsyncSessionLocal() as session:
            await persist_decision(session, result)

        return result

    def health(self):
        return {
            "decision_engine": "ok",
            "faiss_vectors": self.vector_store.health(),
        }

decision_engine = DecisionEngine()
