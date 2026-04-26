from langchain_core.tools import tool  
from pydantic import BaseModel


# --- Input Schemas ---
class SearchInput(BaseModel):
    location: str
    checkin_date: str
    checkout_date: str
    guests: int

class DetailsInput(BaseModel):
    listing_id: int

class BookingInput(BaseModel):
    listing_id: int
    checkin_date: str
    checkout_date: str
    guests: int


# --- Tools ---
@tool(args_schema=SearchInput)
def search_available_properties(
    location: str,
    checkin_date: str,
    checkout_date: str,
    guests: int,
) -> list:
    """Search available properties based on user criteria."""
    return [
        {
            "listing_id": 101,
            "title": "Sea View Apartment",
            "price_per_night": 4500,
            "location": location,
        }
    ]


@tool(args_schema=DetailsInput)
def get_listing_details(listing_id: int) -> dict:
    """Get detailed information about a specific listing."""
    return {
        "listing_id": listing_id,
        "title": "Sea View Apartment",
        "description": "Ocean-facing apartment with balcony",
        "price_per_night": 4500,
        "max_guests": 4,
    }


@tool(args_schema=BookingInput)
def create_booking(
    listing_id: int,
    checkin_date: str,
    checkout_date: str,
    guests: int,
) -> dict:
    """Create a confirmed booking for a listing."""
    return {
        "booking_id": 5001,
        "status": "confirmed",
        "total_price": 9000,
    }