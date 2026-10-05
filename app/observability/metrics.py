from prometheus_client import Counter, Histogram

HTTP_REQUESTS = Counter(
    "jobscout_http_requests_total",
    "Total HTTP requests.",
    ["method", "route", "status"],
)

HTTP_DURATION = Histogram(
    "jobscout_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "route"],
)

CHAT_REQUESTS = Counter(
    "jobscout_chat_requests_total",
    "Total chat requests.",
)

CHAT_ERRORS = Counter(
    "jobscout_chat_errors_total",
    "Total chat errors.",
)

CHAT_DURATION = Histogram(
    "jobscout_chat_duration_seconds",
    "Chat request duration in seconds.",
)

CHAT_MATCHES = Histogram(
    "jobscout_chat_matches",
    "Number of matched jobs returned by a chat request.",
    buckets=(0, 1, 2, 3, 5, 10),
)

LLM_CALLS = Counter(
    "jobscout_llm_calls_total",
    "Total LLM calls.",
    ["provider"],
)
