from langchain_community.tools import tool


# -----------------------------
# Tools
# -----------------------------

@tool
def search_available_properties(
    location: str,
    checkin_date: str,
    checkout_date: str,
    guests: int
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


@tool
def get_listing_details(listing_id: int) -> dict:
    """Get detailed information about a listing."""
    return {
        "listing_id": listing_id,
        "title": "Sea View Apartment",
        "description": "Ocean-facing apartment with balcony",
        "price_per_night": 4500,
        "max_guests": 4,
    }


@tool
def create_booking(
    listing_id: int,
    checkin_date: str,
    checkout_date: str,
    guests: int
) -> dict:
    """Create a booking for a listing."""
    return {
        "booking_id": 5001,
        "status": "confirmed",
        "total_price": 9000,
    }