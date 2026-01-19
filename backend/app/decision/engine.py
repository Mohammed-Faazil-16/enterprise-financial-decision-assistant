from app.retrieval.vector_store import vector_store

class DecisionEngine:
    def __init__(self):
        self.vector_store = vector_store

    def health(self):
        return {
            "decision_engine": "ok",
            "vector_store": self.vector_store.health(),
        }


# EXPORT THAT API EXPECTS
decision_engine = DecisionEngine()
