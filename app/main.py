from fastapi import FastAPI

app = FastAPI(title="LLMOps Chatbot")


@app.get("/health")
def health():
    return {"status": "ok"}
