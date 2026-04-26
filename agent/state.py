from typing import TypedDict, Optional, Dict, Any


class AgentState(TypedDict):
    user_message: str
    intent: Optional[str]
    location: Optional[str]
    checkin_date: Optional[str]
    checkout_date: Optional[str]
    guests: Optional[int]
    listing_id: Optional[int]
    tool_result: Optional[Dict[str, Any]]
    response: Optional[str]