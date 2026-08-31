from prometheus_client import Counter, Histogram


LLM_REQUESTS = Counter(
    "llm_requests_total",
    "Total number of LLM requests",
)

LLM_ERRORS = Counter(
    "llm_errors_total",
    "Total number of LLM errors",
)

LLM_REQUEST_DURATION = Histogram(
    "llm_request_duration_seconds",
    "LLM request duration in seconds",
)

LLM_INPUT_TOKENS = Counter(
    "llm_input_tokens_total",
    "Total number of input tokens",
)

LLM_OUTPUT_TOKENS = Counter(
    "llm_output_tokens_total",
    "Total number of output tokens",
)
