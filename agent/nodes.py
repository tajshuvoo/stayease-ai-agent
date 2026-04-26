from agent.state import AgentState
from agent.tools import (
    search_available_properties,
    get_listing_details,
    create_booking,
)


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
    """Return next node based on intent."""
    if state["intent"] in ["search", "details", "book"]:
        return "tool_node"
    return "fallback_node"


# -----------------------------
# 3. Tool Node
# -----------------------------
def tool_node(state: AgentState) -> AgentState:
    """Execute appropriate tool based on intent."""

    intent = state["intent"]

    if intent == "search":
        result = search_available_properties.invoke({
            "location": state.get("location", "Cox's Bazar"),
            "checkin_date": state.get("checkin_date", "2026-05-01"),
            "checkout_date": state.get("checkout_date", "2026-05-03"),
            "guests": state.get("guests", 2),
        })

    elif intent == "details":
        result = get_listing_details.invoke({
            "listing_id": state.get("listing_id", 101),
        })

    elif intent == "book":
        result = create_booking.invoke({
            "listing_id": state.get("listing_id", 101),
            "checkin_date": state.get("checkin_date", "2026-05-01"),
            "checkout_date": state.get("checkout_date", "2026-05-03"),
            "guests": state.get("guests", 2),
        })

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