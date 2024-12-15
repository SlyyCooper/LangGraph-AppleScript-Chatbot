from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from orchestrator import create_chat_interface
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="LangGraph AppleScript Chatbot")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    response: str
    history: List[ChatMessage]

# Initialize chat interface
chat_fn = create_chat_interface()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Convert history to LangChain message format
        history = []
        if request.history:
            for msg in request.history:
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    history.append(AIMessage(content=msg.content))

        # Get response from chat interface
        messages = chat_fn(request.message, history)
        
        # Convert response back to API format
        response = messages[-1].content
        new_history = [
            ChatMessage(
                role="user" if isinstance(msg, HumanMessage) else "assistant",
                content=msg.content
            )
            for msg in messages
        ]
        
        return ChatResponse(response=response, history=new_history)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 