from travel_state import TravelState
from llm_openrouter import llm, llm_invoke
import json
from langgraph.types import interrupt

class OrchestratorAgent:
    def __init__(self):
       pass

    @classmethod
    def extract_travel_info(cls, state:TravelState):
        input_text = state['input_text']
        prompt = f"""
            Extract the following travel information from the input text:

            Input text:
            {input_text}

            Extract these fields:
            - source_place
            - destination_place
            - from_dates
            - to_dates
            - total_travel_days
            - user_email

            Return ONLY valid JSON using double quotes.

            Expected JSON format:
            {{
                "source_place": "",
                "destination_place": "",
                "from_dates": "",
                "to_dates": "",
                "total_travel_days": 0,
                "user_email": ""
            }}

            Rules:
            1. Do not include any explanation or additional text.
            2. Return only the JSON object.
            3. Ensure the JSON is syntactically valid.
            """.strip()

        response = llm_invoke(prompt)
        travel_info_data = json.loads(response)
        print(f"Extracted travel info: {travel_info_data}")
        return travel_info_data

    @classmethod
    def validate_details(cls, state: TravelState):
        required_fields = [
            "source_place",
            "destination_place",
            "from_dates",
            "total_travel_days",
            "user_email"
        ]

        missing_fields = []

        for field in required_fields:
            value = state.get(field)

            if value is None or value == "":
                missing_fields.append(field)
        print(f"Missing fields: {missing_fields}")
        return {
            "missing_fields": missing_fields
        }

    @classmethod
    def check_missing_fields(cls, state: TravelState):
        print(f"Checking missing fields: {state.get('missing_fields')}")
        if state.get("missing_fields"):
            return "missing"
        else:
            return "complete"

    @classmethod
    def ask_missing_details(cls, state: TravelState):
        missing_fields = state.get("missing_fields") or []
        message = (
            f"Please provide the following details: "
            f"{', '.join(missing_fields)}"
        )
        user_response = interrupt(message)
        current_input = state.get("input_text", "")
        updated_input = f"{current_input} {user_response}".strip()
        return {
            "input_text": updated_input
        }