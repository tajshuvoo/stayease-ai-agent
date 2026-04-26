from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.nodes import (
    parse_intent_node,
    route_next,
    tool_node,
    response_node,
    fallback_node,
)


# -----------------------------
# Build Graph
# -----------------------------
def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("parse_intent", parse_intent_node)
    graph.add_node("tool_node", tool_node)
    graph.add_node("response_node", response_node)
    graph.add_node("fallback_node", fallback_node)

    # Entry
    graph.add_edge(START, "parse_intent")

    # Conditional routing
    graph.add_conditional_edges(
        "parse_intent",
        route_next,
        {
            "tool_node": "tool_node",
            "fallback_node": "fallback_node",
        },
    )

    # Normal flow
    graph.add_edge("tool_node", "response_node")
    graph.add_edge("response_node", END)

    # Fallback flow
    graph.add_edge("fallback_node", END)

    return graph.compile()


# Compile app
app = build_graph()