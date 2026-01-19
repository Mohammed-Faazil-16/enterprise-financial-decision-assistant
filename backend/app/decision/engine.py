from app.agents.graph import build_decision_graph
from app.retrieval.vector_store import vector_store
from app.inference.factory import get_llm_client


class DecisionEngine:
    def __init__(self):
        self.graph = build_decision_graph()
        self.llm = get_llm_client()
        self.vector_store = vector_store

    async def run(self, input_data: dict) -> dict:
        state = {
            "input": input_data,
            "retrieved_evidence": [],
            "analysis": None,
            "decision": None,
            "confidence": None,
            "verification_notes": None,
        }
        result = await self.graph.ainvoke(state)
        return result


# ✅ SINGLE, EXPLICIT EXPORT
decision_engine = DecisionEngine()
