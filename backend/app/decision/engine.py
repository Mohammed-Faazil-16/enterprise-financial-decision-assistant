from app.retrieval.vector_store import vector_store
from app.agents.graph import build_decision_graph

class DecisionEngine:
    def __init__(self):
        self.vector_store = vector_store
        self.graph = build_decision_graph()

    async def decide(self, query: str) -> dict:
        # 1️⃣ Retrieve evidence
        evidence = self.vector_store.search(query, top_k=5)

        # 2️⃣ Initialize agent state
        state = {
            "query": query,
            "evidence": evidence,
        }

        # 3️⃣ Run agent graph
        result = await self.graph.ainvoke(state)
        return result

    def health(self):
        return {
            "decision_engine": "ok",
            "faiss_vectors": self.vector_store.health(),
        }

decision_engine = DecisionEngine()
