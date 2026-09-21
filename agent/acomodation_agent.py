import json
import pandas as pd

class AcomodationAgent:
    def __init__(self):
        pass

    @classmethod
    def get_hotels_options(self, destination_place):
        # Placeholder for accommodation options retrieval logic
        with open('data/mock_hotels.json', 'r') as f:
            hotel_data = json.load(f)
        df = pd.DataFrame(hotel_data)
        hotel_row = df[(df['city'].str.lower() == destination_place.lower())]
        hotel_records = hotel_row.to_dict(orient='records')
        # print(f"Hotel options: {hotel_records}")
        return hotel_records

    @classmethod
    def get_restaurant_options(self, destination_place):
        # Placeholder for accommodation options retrieval logic
        with open('data/mock_restaurants.json', 'r') as f:
            restaurant_data = json.load(f)
        df = pd.DataFrame(restaurant_data)
        restaurant_row = df[(df['city'].str.lower() == destination_place.lower())]
        restaurant_records = restaurant_row.to_dict(orient='records')
        # print(f"Restaurant options: {restaurant_records}")
        return restaurant_records

    @classmethod
    def get_accommodation_details(self, state):
        # Placeholder for accommodation details retrieval logic
        print("Fetching accommodation details based on the extracted travel information...")
        destination_place = state['destination_place']
        hotel_options = self.get_hotels_options(destination_place)
        restaurant_options = self.get_restaurant_options(destination_place)
        print("Accommodation details fetched successfully.")
        return {
            "hotel_options": hotel_options,
            "restaurant_options": restaurant_options
        }
