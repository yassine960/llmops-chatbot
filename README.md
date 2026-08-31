# LLMOps Chatbot

A simple end-to-end LLMOps project exposing a local Qwen LLM through a FastAPI API, with evaluation, monitoring, Docker and CI/CD.

## Architecture

```text
                    ┌──────────────────┐
                    │      Client      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │   /chat /health  │
                    │     /metrics     │
                    └────────┬─────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Qwen2.5-1.5B-Instruct│
                 │      Local LLM       │
                 └───────────────────────┘
                             │
                             │ Metrics
                             ▼
                 ┌───────────────────────┐
                 │      Prometheus       │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │        Grafana        │
                 └───────────────────────┘
```

## Project Goals

The goal of this project is to demonstrate a simple LLMOps workflow covering:

- Local LLM inference
- API serving with FastAPI
- Basic LLM evaluation
- LLM observability
- Prometheus metrics
- Grafana monitoring
- Docker containerization
- Automated testing
- GitHub Actions CI/CD

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **Qwen2.5-1.5B-Instruct**
- **Hugging Face Transformers**
- **PyTorch**
- **Prometheus**
- **Grafana**
- **Docker / Docker Compose**
- **Pytest**
- **GitHub Actions**

## API

The FastAPI application exposes the following endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/chat` | POST | Generate an answer using Qwen |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Swagger API documentation |

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Chat

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is Docker?"}'
```

## Local Development

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

> The first execution downloads the Qwen model from Hugging Face.

## LLM Evaluation

A simple keyword-based evaluation pipeline is included in:

```text
evaluation/
├── dataset.json
└── evaluate.py
```

Run the evaluation with:

```bash
python evaluation/evaluate.py
```

Current baseline result:

```text
Passed: 16/20
Score: 80.0%
```

The evaluation is intentionally simple and serves as a lightweight baseline for measuring whether generated answers contain the expected concepts.

## Observability

The application exposes LLM-specific Prometheus metrics:

- `llm_requests_total`
- `llm_errors_total`
- `llm_request_duration_seconds`
- `llm_input_tokens_total`
- `llm_output_tokens_total`

Example:

```bash
curl http://127.0.0.1:8000/metrics
```

These metrics allow monitoring of:

- Number of LLM requests
- Number of errors
- Request latency
- Input token usage
- Output token usage

## Docker

Build the application image:

```bash
docker compose build
```

Start the complete stack:

```bash
docker compose up
```

The stack contains:

```text
llmops-app
llmops-prometheus
llmops-grafana
```

### Services

| Service | URL |
|---|---|
| FastAPI | http://127.0.0.1:8000 |
| Swagger | http://127.0.0.1:8000/docs |
| Metrics | http://127.0.0.1:8000/metrics |
| Prometheus | http://127.0.0.1:9090 |
| Grafana | http://127.0.0.1:3000 |

Prometheus collects metrics from the FastAPI application, while Grafana is used to visualize them.

## Testing

Run the API tests with:

```bash
python -m pytest -v tests
```

Current test coverage includes the API health endpoint.

The test suite is deliberately lightweight and does not load the Qwen model during test collection.

## CI/CD

GitHub Actions is configured in:

```text
.github/workflows/ci.yml
```

The CI pipeline runs automatically on:

- Pushes to `main`
- Pull requests targeting `main`

The pipeline performs:

1. Python environment setup
2. Dependency installation
3. Python syntax validation
4. Pytest execution

The CI deliberately does not run the full Qwen inference or evaluation pipeline, keeping the CI fast and lightweight.

## Project Structure

```text
llmops-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── llm.py
│   └── metrics.py
│
├── evaluation/
│   ├── dataset.json
│   └── evaluate.py
│
├── monitoring/
│   └── prometheus.yml
│
├── tests/
│   └── test_api.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Results

The project currently demonstrates:

- Local Qwen inference
- FastAPI serving
- `16/20` evaluation score (**80%**)
- Prometheus LLM metrics
- Grafana monitoring
- Docker Compose deployment
- Automated API testing
- Successful GitHub Actions CI

## Scope

This project intentionally focuses on a simple LLMOps architecture.

Advanced components such as RAG, Kubernetes, distributed tracing, model fine-tuning and advanced evaluation frameworks are outside the current scope.