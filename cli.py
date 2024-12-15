from orchestrator import create_chat_interface
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

def print_message(message):
    """Print a message with appropriate formatting based on role."""
    if isinstance(message, AIMessage):
        role = "🤖 Assistant"
        if hasattr(message, "tool_calls") and message.tool_calls:
            print(f"\n{role}: {message.content}")
            for tool_call in message.tool_calls:
                print(f"Tool Call: {tool_call['name']}")
                print(f"Args: {tool_call['args']}")
            return
    elif isinstance(message, ToolMessage):
        role = "🛠️ Tool"
        print(f"\n{role}: {message.content}")
        return
    else:
        role = "👤 You"
    print(f"\n{role}: {message.content}")

def main():
    print("\n🤖 Welcome to the LangGraph AppleScript Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation")
    print("To execute AppleScript, start your message with 'execute applescript:'")
    print("Example: execute applescript: tell application \"Finder\" to get name of every window\n")

    chat_fn = create_chat_interface()
    history = []

    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print("\n🤖 Goodbye! Have a great day!")
                break

            # Get chatbot response
            messages = chat_fn(user_input, history)
            
            # Update history and print new messages
            history = messages
            for message in messages:
                print_message(message)

        except KeyboardInterrupt:
            print("\n\n🤖 Goodbye! Have a great day!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 