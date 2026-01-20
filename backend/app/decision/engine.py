from app.agents.graph import build_decision_graph
from app.retrieval.service import retrieve_top_k

class DecisionEngine:
    def __init__(self):
        self.graph = build_decision_graph()

    async def decide(self, query: str):
        evidence = await retrieve_top_k(query, top_k=3)

        state = {
            "query": query,
            "evidence": evidence,
        }

        result = await self.graph.ainvoke(state)
        return result

decision_engine = DecisionEngine()
