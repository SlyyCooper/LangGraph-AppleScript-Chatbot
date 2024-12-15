import subprocess
from typing import Dict, Any
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage

class AppleScriptAgent:
    def __init__(self):
        self.name = "AppleScript Agent"

    def execute_applescript(self, script: str) -> str:
        """Execute an AppleScript command and return the result."""
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing AppleScript: {e.stderr}"

    async def plan(self, messages: list[BaseMessage], **kwargs) -> AgentAction | AgentFinish:
        """Plan the next action based on the conversation history."""
        last_message = messages[-1].content
        
        if "execute" in last_message.lower() and "applescript" in last_message.lower():
            # Extract AppleScript command from the message
            # This is a simple implementation - you might want to add more sophisticated parsing
            script = last_message.split("execute applescript:", 1)[-1].strip()
            return AgentAction(
                tool="execute_applescript",
                tool_input=script,
                log=f"Executing AppleScript: {script}"
            )
        
        return AgentFinish(
            return_values={"output": "I can help you execute AppleScript commands. Please provide a command with 'execute applescript:' prefix."},
            log="No AppleScript command detected."
        ) 