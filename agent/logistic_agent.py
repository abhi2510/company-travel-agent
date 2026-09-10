import json
import pandas as pd
from travel_state import TravelState

class LogisticAgent:
    def __init__(self):
        pass

    @classmethod
    def get_train_details(cls, source, destination):
        with open('data/mock_trains.json', 'r') as f:
            train_data = json.load(f)
        df = pd.DataFrame(train_data)
        train_row = df[(df['source'] == source) & (df['destination'] == destination)]
        train_records = train_row.to_dict(orient='records')
        print(f"Train details: {train_records}")
        return train_records

    @classmethod
    def get_bus_details(cls, source, destination):
        with open('data/mock_buses.json', 'r') as f:
            bus_data = json.load(f)
        df = pd.DataFrame(bus_data)
        bus_row = df[(df['source'] == source) & (df['destination'] == destination)]
        bus_records = bus_row.to_dict(orient='records')
        print(f"Bus details: {bus_records}")
        return bus_records

    @classmethod
    def get_flight_details(cls, source, destination):
        with open('data/mock_flights.json', 'r') as f:
            flight_data = json.load(f)
        df = pd.DataFrame(flight_data)
        flight_row = df[(df['source'] == source) & (df['destination'] == destination)]
        flight_records = flight_row.to_dict(orient='records')
        print(f"Flight details: {flight_records}")
        return flight_records
    
    @classmethod
    def get_travel_budget(cls, state: TravelState):
        source = state['source_place']
        destination = state['destination_place']
        # ---- Get flight details ----
        outbound_flight_details = cls.get_flight_details(source, destination)
        inbound_flight_details = cls.get_flight_details(destination, source)
        # ---- Get bus details ----
        outbound_bus_details = cls.get_bus_details(source, destination)
        inbound_bus_details = cls.get_bus_details(destination, source)
        # ---- Get train details ----
        outbound_train_details = cls.get_train_details(source, destination)
        inbound_train_details = cls.get_train_details(destination, source)

        return {
            "outbound_flight_details": outbound_flight_details,
            "inbound_flight_details": inbound_flight_details,
            "outbound_bus_details": outbound_bus_details,
            "inbound_bus_details": inbound_bus_details,
            "outbound_train_details": outbound_train_details,
            "inbound_train_details": inbound_train_details
        }