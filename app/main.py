from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import generate_response


app = FastAPI(title="LLMOps Chatbot")


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = generate_response(request.message)

    return {
        "response": response
    }
