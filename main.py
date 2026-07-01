from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent.core import run_agent

app = FastAPI(title="Multi-Tool AI Agent API")

# In-memory session store
sessions: dict[str, list] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = Field(default="default")

class ChatResponse(BaseModel):
    response: str
    tools_used: list[str]
    session_id: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    if len(request.message) > 1000:
        raise HTTPException(status_code=400, detail="Message too long (max 1000 characters).")

    # Get or create session
    history = sessions.get(request.session_id, [])


    result = run_agent(request.message, history=history)

    sessions[request.session_id] = result["messages"]

    return ChatResponse(
        response=result["response"],
        tools_used=result["tools_used"],
        session_id=request.session_id,
    )
