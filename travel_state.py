from typing import TypedDict

class TravelState(TypedDict):
    input_text: str
    user_email: str
    source_place: str
    destination_place: str
    from_dates: str
    to_dates: str
    total_travel_days: int
    budget: float
    preferences: list[str]