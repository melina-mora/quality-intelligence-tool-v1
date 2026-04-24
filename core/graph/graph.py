from langgraph.graph import StateGraph, START, END
from core.graph.state import ReviewState
from core.graph import nodes


def build_graph():
    graph = StateGraph(ReviewState)

    #Utility nodes
    graph.add_node("Sync", nodes.node_sync)

    #Main nodes
    graph.add_node("XML Parser", nodes.node_xml_parser)
    graph.add_node("CSV Parser", nodes.node_csv_parser)
    graph.add_node("Metrics", nodes.node_metrics)
    graph.add_node("Quality Gates", nodes.node_quality_gates)
    graph.add_node("AI analyzer", nodes.node_ai_analyzer)
    graph.add_node("Output", nodes.node_output)

    #Start---------------
    graph.add_edge(START, "XML Parser")
    graph.add_edge(START, "CSV Parser")

    #Phase 1
    graph.add_edge("XML Parser", "AI analyzer")
    graph.add_edge("XML Parser", "Metrics")

    #multiple inputs with Sync (avoid race conditions)
    graph.add_edge("CSV Parser", "Sync")
    graph.add_edge("Metrics", "Sync")
    graph.add_edge("Sync", "Quality Gates")

    #Phase 2
    graph.add_edge("Metrics", "Output")
    graph.add_edge("Quality Gates", "Output")
    graph.add_edge("AI analyzer", "Output")

    #Output
    graph.add_edge("Output", END)

    return graph.compile()