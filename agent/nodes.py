from agent.state import AgentState


# -----------------------------
# 1. Parse Intent Node
# -----------------------------
def parse_intent_node(state: AgentState) -> AgentState:
    """Extract intent from user message."""
    message = state["user_message"].lower()

    if "book" in message:
        intent = "book"
    elif "detail" in message or "tell me about" in message:
        intent = "details"
    elif "room" in message or "hotel" in message:
        intent = "search"
    else:
        intent = "fallback"

    return {
        **state,
        "intent": intent,
    }


# -----------------------------
# 2. Routing Function
# -----------------------------
def route_next(state: AgentState) -> str:
    """Return next node name based on intent."""
    if state["intent"] in ["search", "details", "book"]:
        return "tool_node"
    return "fallback_node"


# -----------------------------
# 3. Tool Node
# -----------------------------
def tool_node(state: AgentState) -> AgentState:
    """Simulate tool execution based on intent."""
    intent = state["intent"]

    # NOTE: In real implementation, LangChain tools would be called here

    if intent == "search":
        result = {
            "listings": [
                {"id": 101, "title": "Sea View Apartment", "price": 4500}
            ]
        }

    elif intent == "details":
        result = {
            "listing": {
                "id": state.get("listing_id", 101),
                "title": "Sea View Apartment",
                "description": "Ocean-facing apartment",
                "price": 4500,
            }
        }

    elif intent == "book":
        result = {
            "booking": {
                "id": 5001,
                "status": "confirmed",
                "total_price": 9000,
            }
        }

    else:
        result = {}

    return {
        **state,
        "tool_result": result,
    }


# -----------------------------
# 4. Response Node
# -----------------------------
def response_node(state: AgentState) -> AgentState:
    """Format final response."""
    return {
        **state,
        "response": str(state.get("tool_result", {})),
    }


# -----------------------------
# 5. Fallback Node
# -----------------------------
def fallback_node(state: AgentState) -> AgentState:
    """Handle unsupported queries."""
    return {
        **state,
        "response": "Request not supported. Escalating to human agent.",
    }