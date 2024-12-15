from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from agents.applescript_agent import AppleScriptAgent
from langchain_core.tools import tool
from langgraph.prebuilt import ToolExecutor
import config

# Define our state
class State(TypedDict):
    messages: Annotated[list, add_messages]

def create_graph():
    # Create the graph
    graph = StateGraph(State)
    
    # Initialize our chat model
    llm = ChatAnthropic(
        api_key=config.ANTHROPIC_API_KEY,
        model="claude-3-opus-20240229"
    )
    
    # Initialize AppleScript agent
    applescript_agent = AppleScriptAgent()
    
    # Create our AppleScript tool
    @tool
    def execute_applescript(script: str) -> str:
        """Execute an AppleScript command."""
        return applescript_agent.execute_applescript(script)
    
    # Create tool executor
    tools = [execute_applescript]
    tool_executor = ToolExecutor(tools)
    
    # Bind the tool to our LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the chatbot node
    def chatbot(state: State):
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        
        # If the response has tool calls, execute them
        if hasattr(response, "tool_calls") and response.tool_calls:
            tool_results = []
            for tool_call in response.tool_calls:
                result = tool_executor.execute(
                    tool_call["name"],
                    tool_call["args"]
                )
                tool_results.append(result)
            
            # Create a new response with tool results
            final_response = llm_with_tools.invoke(
                messages + [response] + [{"role": "tool", "content": str(r)} for r in tool_results]
            )
            return {"messages": [response] + [{"role": "tool", "content": str(r)} for r in tool_results] + [final_response]}
        
        return {"messages": [response]}
    
    # Add the chatbot node
    graph.add_node("chatbot", chatbot)
    
    # Add edges
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", END)
    
    return graph.compile()

def create_chat_interface():
    """Create a chat interface."""
    graph = create_graph()
    
    def chat(message: str, chat_history: list[BaseMessage] = None) -> list[BaseMessage]:
        if chat_history is None:
            chat_history = []
        
        # Create a proper HumanMessage
        human_message = HumanMessage(content=message)
        
        state = {"messages": chat_history + [human_message]}
        result = graph.invoke(state)
        return result["messages"]
    
    return chat 