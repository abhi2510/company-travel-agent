from langgraph.graph import StateGraph, START, END
from travel_state import TravelState
from agent.orchestrator_agent import OrchestratorAgent
from agent.travelPolicy_agent import TravelPolicyAgent
graph = StateGraph(TravelState)

#create nodes
graph.add_node('extract_travel_info', OrchestratorAgent.extract_travel_info)
graph.add_node('get_travel_budget', TravelPolicyAgent.get_travel_budget)

# create edges
graph.add_edge(START, 'extract_travel_info')
graph.add_edge('extract_travel_info', 'get_travel_budget')
graph.add_edge('get_travel_budget', END)

#workflow execution
workflow = graph.compile()
print(workflow)

# initial_state = {
#     'input_text': "I want to travel from New York to Los Angeles from 2023-10-01 to 2023-10-10. My Email id is abhishek.kumar@example.com.",
# }

# workflow.invoke(initial_state)