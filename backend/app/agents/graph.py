from langgraph.graph import StateGraph, END
from app.agents import planner, analyzer, verifier, finalizer

def build_decision_graph():
    graph = StateGraph(dict)

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
