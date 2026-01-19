from langgraph.graph import StateGraph, END
from app.agents.planner import PlannerAgent
from app.agents.analyzer import AnalyzerAgent
from app.agents.verifier import VerifierAgent
from app.agents.finalizer import FinalizerAgent

def build_decision_graph():
    graph = StateGraph(dict)  # note: dict type
    planner = PlannerAgent()
    analyzer = AnalyzerAgent()
    verifier = VerifierAgent()
    finalizer = FinalizerAgent()

    graph.add_node("planner", planner.run)
    graph.add_node("analyzer", analyzer.run)
    graph.add_node("verifier", verifier.run)
    graph.add_node("finalizer", finalizer.run)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "analyzer")
    graph.add_edge("analyzer", "verifier")
    graph.add_edge("verifier", "finalizer")
    graph.add_edge("finalizer", END)

    return graph.compile()
