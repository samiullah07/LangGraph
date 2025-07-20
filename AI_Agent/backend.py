from pydantic import BaseModel
from typing import List
from fastapi import FastAPI

class AI_Agent(BaseModel):
    llm_id: str
    llm_provider: str
    search_result: bool
    system_prompt: str
    messages:List[str]


Allowed_models = ["llama-3.1-8b-instant", "llama-3.1-70b-instant","gpt3.5-turbo","gpt-4o","gpt-4o-mini"]
app = FastAPI(title="AI Agent API")

@app.post("/chat")
def chat_with_agent(agent: AI_Agent):
    """
    Endpoint to chat with the AI agent.
    """

    if agent.llm_id not in Allowed_models:
        return {"error": "Model not allowed. Please choose a valid model."}


    from ai_agent import create_agent
    response = create_agent(
        llm_id=agent.llm_id,
        llm_provider=agent.llm_provider,
        search_result=agent.search_result,
        query=agent.messages,
        system_prompt=agent.system_prompt
    )
    return {"response": response}

