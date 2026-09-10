from graph_workflow import workflow

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "thanks", "thank you"]:
            break
        workflow.invoke({'input_text': user_input})