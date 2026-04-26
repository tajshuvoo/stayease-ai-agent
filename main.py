from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent.graph import app as agent_app
from agent.state import AgentState

app = FastAPI(title="StayEase AI Agent")

# In-memory store (replace with PostgreSQL for production)
conversations: dict[str, list] = {}


class MessageRequest(BaseModel):
    message: str


@app.post("/api/chat/{conversation_id}/message")
async def send_message(conversation_id: str, request: MessageRequest):
    """Send a guest message to the AI agent."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Invalid input message")

    if conversation_id not in conversations:
        conversations[conversation_id] = []

    initial_state: AgentState = {
        "user_message": request.message,
        "intent": None,
        "location": None,
        "checkin_date": None,
        "checkout_date": None,
        "guests": None,
        "listing_id": None,
        "tool_result": None,
        "response": None,
    }

    result = agent_app.invoke(initial_state)

    conversations[conversation_id].append({"role": "user", "content": request.message})
    conversations[conversation_id].append({"role": "assistant", "content": result["response"]})

    return {
        "response": result["response"],
        "data": result.get("tool_result"),
    }


@app.get("/api/chat/{conversation_id}/history")
async def get_history(conversation_id: str):
    """Retrieve full conversation history."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id],
    }