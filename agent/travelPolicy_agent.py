import json
import pandas as pd
from travel_state import TravelState


class TravelPolicyAgent:
    def __init__(self):
        pass

    @classmethod
    def get_employee_salary(cls, employee_email):
        with open('data/employee_details.json', 'r') as f:
            employee_data = json.load(f)
        df = pd.DataFrame(employee_data)
        employee_row = df[df['Email'] == employee_email]
        if not employee_row.empty:
            salary = employee_row['Salary'].values[0]
            return salary
        else:
            print(f"No employee found with email: {employee_email}")
        return None

    @classmethod
    def get_travel_budget(cls, state: TravelState):
        employee_email = state['user_email']
        total_travel_days = state['total_travel_days']
        final_budget = 0
        salary = cls.get_employee_salary(employee_email)
        if salary is not None:
            with open('data/travel_policy.json', 'r') as f:
                travel_policy = json.load(f)
            
            policy_budget = travel_policy.get("tiers", 0)
            df_budget = pd.DataFrame(policy_budget)
            budget_row = df_budget[(df_budget['min_salary_lpa'] <= salary) & (df_budget['max_salary_lpa'] > salary)]
            if not budget_row.empty:
                daily_budget = budget_row['daily_budget'].values[0]
                if daily_budget is not None:
                    final_budget = daily_budget * total_travel_days  # Assuming 30 days in a month
                print(f"Travel Budget: {final_budget}")
        return {"budget": final_budget}