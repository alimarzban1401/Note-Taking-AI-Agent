# evaluate_agent.py
from agent import app
import uuid

def run_test_case(name, user_input):
    print(f"\n Testing: {name}")
    print(f"User Input: '{user_input}'")
    
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    events = app.stream({"messages": [("user", user_input)]}, config)
    for event in events:
        for value in event.values():
            if "messages" in value:
                msg = value['messages'][-1]
                # Only print if there's actual text and it's not a raw tool instruction
                if msg.content and not msg.tool_calls:
                    # If content is a list (typical for Claude), get the text part
                    if isinstance(msg.content, list):
                        text = next((item['text'] for item in msg.content if item.get('type') == 'text'), "")
                        if text: print(f" Result: {text}")
                    else:
                        print(f" Result: {msg.content}")
    print("-" * 50)

if __name__ == "__main__":
    print("--- STARTING AUTOMATED EVALUATION ---")
    run_test_case("Complex Creation", "Save a note about Python decorators with the tag 'coding'.")
    run_test_case("Search Test", "What notes do I have about coding?")
    print("--- EVALUATION COMPLETE ---")