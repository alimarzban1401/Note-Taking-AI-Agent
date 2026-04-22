import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from tools import create_note, search_notes, update_note, delete_note

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

tools = [create_note, search_notes, update_note, delete_note]
tool_node = ToolNode(tools)

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def call_model(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def should_continue(state: State):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return END
    return "tools"

workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

# --- THE UPGRADE ---
# We tell the graph: "Stop and wait before running the 'tools' node"
memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory, 
    interrupt_before=["tools"] 
)

def run_chat():
    config = {"configurable": {"thread_id": "user_1"}}
    print("\n" + "="*40)
    print("      NOTE-TAKING AGENT IS ONLINE")
    print("="*40)
    
    while True:
        state = app.get_state(config)
        
        if state.next:
            last_msg = state.values["messages"][-1]
            tool_name = last_msg.tool_calls[0]['name']
            
            if tool_name in ["delete_note", "update_note"]:
                confirm = input(f"\n [SAFETY CHECK] The agent wants to {tool_name}. Proceed? (y/n): ")
                if confirm.lower() != 'y':
                    print("Action cancelled by user.")
                    app.update_state(config, {"messages": [("user", "Cancel that action.")]})
                    continue 
            
            for event in app.stream(None, config): 
                for value in event.values():
                    if "messages" in value:
                        # Only print the text, ignore the JSON tool calls
                        content = value['messages'][-1].content
                        if content: print(f"\nAgent: {content}")
            continue

        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]: break
            
        for event in app.stream({"messages": [("user", user_input)]}, config):
            for value in event.values():
                if "messages" in value:
                    msg = value['messages'][-1]
                    # This check skips printing the raw JSON tool_calls
                    if msg.content and not msg.tool_calls:
                        print(f"\nAgent: {msg.content}")

if __name__ == "__main__":
    run_chat()