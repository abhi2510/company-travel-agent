from travel_state import TravelState
from llm_openrouter import llm
import json

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
            3. Use an empty string "" if a value cannot be determined.
            4. Use 0 for total_travel_days if it cannot be determined.
            5. Ensure the JSON is syntactically valid.
            """.strip()

        response = llm.invoke(prompt)
        travel_info_data = json.loads(response.content.strip())
        print(f"Extracted travel info: {travel_info_data}")
        return travel_info_data
