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
    outbound_flight_details: list[dict]
    inbound_flight_details: list[dict]
    outbound_bus_details: list[dict]
    inbound_bus_details: list[dict]
    outbound_train_details: list[dict]
    inbound_train_details: list[dict]
    preferences: list[str]