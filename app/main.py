import time

from fastapi import FastAPI
from prometheus_client import make_asgi_app
from pydantic import BaseModel

from app.metrics import (
    LLM_ERRORS,
    LLM_INPUT_TOKENS,
    LLM_OUTPUT_TOKENS,
    LLM_REQUEST_DURATION,
    LLM_REQUESTS,
)


app = FastAPI(title="LLMOps Chatbot")


class ChatRequest(BaseModel):
    message: str


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    from app.llm import generate_response
    LLM_REQUESTS.inc()

    start_time = time.perf_counter()

    try:
        response, input_tokens, output_tokens = generate_response(
            request.message
        )

        LLM_INPUT_TOKENS.inc(input_tokens)
        LLM_OUTPUT_TOKENS.inc(output_tokens)

        return {
            "response": response,
        }

    except Exception:
        LLM_ERRORS.inc()
        raise

    finally:
        duration = time.perf_counter() - start_time
        LLM_REQUEST_DURATION.observe(duration)
