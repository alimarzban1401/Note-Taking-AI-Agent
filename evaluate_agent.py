# evaluate_agent.py
from agent import app
import uuid

def run_test_case(name, user_input, thread_id=None):
    print(f"\n Testing: {name}")
    # Share thread_id for multi-turn tests, otherwise fresh ID
    t_id = thread_id if thread_id else str(uuid.uuid4())
    config = {"configurable": {"thread_id": t_id}}
    
    try:
        # invoke is safer for tests because it waits for tools to finish
        result = app.invoke({"messages": [("user", user_input)]}, config)
        last_msg = result["messages"][-1]
        
        # Check for interrupt/safety
        state = app.get_state(config)
        status = "[INTERRUPT]" if state.next else "[SUCCESS]"
        
        # Clean printing logic
        content = last_msg.content
        if isinstance(content, list):
            text = next((item['text'] for item in content if item.get('type') == 'text'), "Action performed.")
        else:
            text = content if content else "Action performed."
            
        print(f"  {status} Result: {text[:120]}...")
    except Exception as e:
        print(f" Error: {str(e)[:50]}")
    
    return t_id

if __name__ == "__main__":
    print("--- STARTING 12-POINT EVALUATION HARNESS ---")

    # Happy Paths & Multi-turn
    tid = run_test_case("Creation", "Save a note 'Python' about decorators.")
    run_test_case("Follow-up (Memory)", "Add the tag 'coding' to that last note.", thread_id=tid)
    
    # Required Behaviors
    run_test_case("Search", "What do I have about Python?")
    run_test_case("Disambiguation", "Update the note.")
    run_test_case("Summarize", "Summarize all my notes.")

    # Edge Cases
    run_test_case("No Results", "Find a note about dragons.")
    run_test_case("Nonsense", "!!!???!!!")
    run_test_case("Empty", "Search for ''")

    # Safety Checks
    run_test_case("Delete Safety", "Delete the Python note.")
    run_test_case("Update Safety", "Change the title of my note to 'New Title'.")

    # Reasoning
    run_test_case("Contradiction", "Do I have any notes that contradict each other?")
    run_test_case("Tag Search", "Show me all 'coding' notes.")

    print("\n--- EVALUATION COMPLETE ---")