import os
import json
from groq import Groq
from dotenv import load_dotenv

from agent.state import AgentState
from agent.tools import (
    search_available_properties,
    get_listing_details,
    create_booking,
)

load_dotenv()

# Groq client — API key loaded from .env
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# -----------------------------
# 1. Parse Intent Node
# -----------------------------
def parse_intent_node(state: AgentState) -> AgentState:
    """Extract intent and entities from user message using Groq LLM."""
    message = state["user_message"]

    prompt = f"""You are an intent parser for a hotel booking assistant.
Extract the following from the user message and return ONLY a valid JSON object — no explanation, no markdown.

Fields:
- intent: one of "search", "details", "book", "fallback"
- location: string or null
- checkin_date: string (YYYY-MM-DD) or null
- checkout_date: string (YYYY-MM-DD) or null
- guests: integer or null
- listing_id: integer or null

User message: "{message}"
"""

    completion = groq_client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_completion_tokens=256,
        top_p=0.95,
        reasoning_effort="default",
        stream=False,
        stop=None,
    )

    raw = completion.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"intent": "fallback"}

    return {
        **state,
        "intent": parsed.get("intent", "fallback"),
        "location": parsed.get("location"),
        "checkin_date": parsed.get("checkin_date"),
        "checkout_date": parsed.get("checkout_date"),
        "guests": parsed.get("guests"),
        "listing_id": parsed.get("listing_id"),
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
    """Execute the appropriate tool based on intent."""
    intent = state["intent"]

    if intent == "search":
        result = search_available_properties.invoke({
            "location": state.get("location") or "Cox's Bazar",
            "checkin_date": state.get("checkin_date") or "2026-05-01",
            "checkout_date": state.get("checkout_date") or "2026-05-03",
            "guests": state.get("guests") or 2,
        })
    elif intent == "details":
        result = get_listing_details.invoke({
            "listing_id": state.get("listing_id") or 101,
        })
    elif intent == "book":
        result = create_booking.invoke({
            "listing_id": state.get("listing_id") or 101,
            "checkin_date": state.get("checkin_date") or "2026-05-01",
            "checkout_date": state.get("checkout_date") or "2026-05-03",
            "guests": state.get("guests") or 2,
        })
    else:
        result = {}

    return {**state, "tool_result": result}


# -----------------------------
# 4. Response Node
# -----------------------------
def response_node(state: AgentState) -> AgentState:
    """Format tool result into a natural language reply using Groq LLM."""
    tool_result = state.get("tool_result", {})
    intent = state.get("intent", "")

    prompt = f"""You are a helpful booking assistant for StayEase, a rental platform in Bangladesh.
The user's intent was: {intent}
Tool result: {json.dumps(tool_result, ensure_ascii=False)}

Write a short, friendly response in English. Use BDT for prices. Be concise."""

    completion = groq_client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=512,
        top_p=0.95,
        reasoning_effort="default",
        stream=False,
        stop=None,
    )

    response_text = completion.choices[0].message.content.strip()
    return {**state, "response": response_text}


# -----------------------------
# 5. Fallback Node
# -----------------------------
def fallback_node(state: AgentState) -> AgentState:
    """Handle unsupported queries by escalating to a human agent."""
    return {
        **state,
        "response": "I'm sorry, I can only help with property search, listing details, or bookings. Escalating to a human agent.",
    }