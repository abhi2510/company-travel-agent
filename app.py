from graph_workflow import workflow
from langgraph.types import Command
import uuid

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "thanks", "thank you"]:
            break

        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        state = {"input_text": user_input}

        while True:
            result = workflow.invoke(state, config=config)

            if "__interrupt__" in result:
                interrupt_payload = result["__interrupt__"][0]
                print(interrupt_payload.value)
                follow_up = input("Provide the missing detail: ").strip()
                if follow_up.lower() in ["exit", "quit", "thanks", "thank you"]:
                    raise SystemExit
                state = Command(resume=follow_up)
                continue

            print(result)
            break