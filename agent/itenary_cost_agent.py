import json
from itertools import product
from travel_state import TravelState
from llm_openrouter import llm, llm_invoke

class ItenaryCostAgent:
    def __init__(self):
        pass

    @classmethod
    def generate_combined_options(cls, outbound_options, inbound_options, hotel_options, restaurant_options, number_of_nights, number_of_days, meals_per_day, budget):
        travel_options = []
        for outbound, inbound, hotel, restaurant in product(outbound_options, inbound_options, 
            hotel_options, restaurant_options
        ):
            outbound_cost = outbound["cost"]
            inbound_cost = inbound["cost"]
            hotel_cost = hotel.get("price_per_night", 0) * number_of_nights
            restaurant_cost = restaurant.get("average_meal_price", 0) * meals_per_day * number_of_days
            total_cost = outbound_cost + inbound_cost + hotel_cost + restaurant_cost
            # print(f"Total cost: {total_cost}, Budget: {budget}, Outbound: {outbound_cost}, Inbound: {inbound_cost}, Hotel: {hotel_cost}, Restaurant: {restaurant_cost}")

            travel_options.append({
                "outbound": outbound,
                "inbound": inbound,
                "hotel": hotel,
                "restaurant": restaurant,
                "outbound_cost": outbound_cost,
                "inbound_cost": inbound_cost,
                "hotel_cost": hotel_cost,
                "restaurant_cost": restaurant_cost,
                "total_cost": total_cost,
                "budget_difference": budget - total_cost
            })
        # print(f"Travel options value: {len(travel_options)}")
        return travel_options

    @classmethod
    def combine_outbound_options(cls, outbound_flights, outbound_buses, outbound_trains):
        outbound_options = []
        # print(f"Outbound flights: {len(outbound_flights)}, Outbound buses: {len(outbound_buses)}, Outbound trains: {len(outbound_trains)}")
        for flight in outbound_flights:
            outbound_options.append({"mode": "flight", "details": flight, "cost": float(flight.get("price", 0))})
        for bus in outbound_buses:
            outbound_options.append({"mode": "bus", "details": bus, "cost": float(bus.get("price", 0))})
        for train in outbound_trains:
            outbound_options.append({"mode": "train", "details": train, "cost": float(train.get("price", 0))})
        # print(f"Outbound options value: {len(outbound_options)}")
        return outbound_options

    @classmethod
    def combine_inbound_options(cls, inbound_flights, inbound_buses, inbound_trains):
        inbound_options = []
        print(f"Inbound flights: {len(inbound_flights)}, Inbound buses: {len(inbound_buses)}, Inbound trains: {len(inbound_trains)}")
        for flight in inbound_flights:
            inbound_options.append({"mode": "flight", "details": flight, "cost": float(flight.get("price", 0))})
        for bus in inbound_buses:
            inbound_options.append({"mode": "bus", "details": bus, "cost": float(bus.get("price", 0))})
        for train in inbound_trains:
            inbound_options.append({"mode": "train", "details": train, "cost": float(train.get("price", 0))})
        # print(f"Inbound options value: {len(inbound_options)}")
        return inbound_options

    @classmethod
    def calculate_itenary_options(cls, budget, outbound_flights, inbound_flights, outbound_buses, inbound_buses, outbound_trains,
            inbound_trains,hotels, restaurants, number_of_nights, number_of_days, meals_per_day):
        outbound_options = cls.combine_outbound_options(outbound_flights, outbound_buses, outbound_trains)
        inbound_options = cls.combine_inbound_options(inbound_flights, inbound_buses, inbound_trains)
        travel_options = cls.generate_combined_options(outbound_options, inbound_options, hotels, restaurants, number_of_nights, 
                                    number_of_days, meals_per_day, budget)

        # print(f"Total travel options generated: {len(travel_options)}")
        # Sort by total cost
        travel_options.sort(key=lambda x: x["total_cost"])

        # print(f"Sorted travel options generated: {len(travel_options)}")

        # Options within budget
        within_budget = [option for option in travel_options if option["total_cost"] <= budget]

        # Best within budget
        best_option = (within_budget[-1] if within_budget else None)

        # Closest to budget# 
        closest_option = (min(
            travel_options,
            key=lambda x: abs(x["total_cost"] - budget)
            ) if travel_options else None)

        return {
            "best_option": best_option,
            "closest_option": closest_option,
            "all_options": travel_options
        }

    
    @classmethod
    def generate_itinerary(cls, state: TravelState):
        print("Generating itinerary and calculating total cost based on the extracted travel information...")

        budget = state['budget']
        outbound_flight_details = state['outbound_flight_details']
        inbound_flight_details = state['inbound_flight_details']
        outbound_bus_details = state['outbound_bus_details']
        inbound_bus_details = state['inbound_bus_details']
        outbound_train_details = state['outbound_train_details']
        inbound_train_details = state['inbound_train_details']
        hotel_options = state['hotel_options']
        restaurant_options = state['restaurant_options']
        number_of_nights = state['total_travel_days'] - 1
        number_of_days = state['total_travel_days']
        meals_per_day = 3  # Assuming 3 meals per day

        # print(f"In Iternanry Budget: {budget}, Outbound flights: {len(outbound_flight_details)}, Inbound flights: {len(inbound_flight_details)}, Outbound buses: {len(outbound_bus_details)}, Inbound buses: {len(inbound_bus_details)}, Outbound trains: {len(outbound_train_details)}, Inbound trains: {len(inbound_train_details)}, Hotels: {len(hotel_options)}, Restaurants: {len(restaurant_options)}")

        results = cls.calculate_itenary_options(
            budget,
            outbound_flight_details,
            inbound_flight_details,
            outbound_bus_details,
            inbound_bus_details,
            outbound_train_details,
            inbound_train_details,
            hotel_options,
            restaurant_options,
            number_of_nights,
            number_of_days,
            meals_per_day
        )

        best_option = results["best_option"]
        closest_option = results["closest_option"]

        prompt = f"""
            You are a corporate travel planner.

            Create a concise itinerary summary using ONLY the data provided below.

            Budget: ₹{budget}

            Best option within budget:
            {json.dumps(best_option, indent=2, ensure_ascii=False)}

            Closest option to budget:
            {json.dumps(closest_option, indent=2, ensure_ascii=False)}

            Rules:
            - Do not recalculate or modify any prices.
            - Use the exact total_cost provided.
            - Do not invent any information.
            - Clearly mention whether the selected option is within budget.
            - Return plain text only.

            Required format:

            Best option within budget:
            Outbound travel: ...
            Inbound travel: ...
            Accommodation: ...
            Restaurant: ...
            Total cost: ...
            Budget remaining: ...
            Total Budget: ...

            Closest option to budget:
            Outbound travel: ...
            Inbound travel: ...
            Accommodation: ...
            Restaurant: ...
            Total cost: ...
            Budget difference: ...
            Total Budget: ...

            Final recommendation:
            ...
        """

        response = llm_invoke(prompt)
        print(f"LLM response: {response}")
        print("Itinerary generated and total cost calculated successfully.")
        return {"itenary_info_details": response.strip() }