# JobScout AI - C12 Reference Application

JobScout AI is a small, course-owned job-search assistant used as the reference application for C12: System Design, DevOps and Cloud Deployment.

The application is intentionally ready before learners start Sprint 2. The course focuses on the infrastructure and operational concerns around the application rather than on building its business functionality.

## Application capabilities already present

- `POST /chat` - multi-step job search assistant flow
- `GET /health` - service health check
- `GET /metrics` - Prometheus-format application metrics
- Multi-step agent workflow with clearly separated steps
- LLM provider abstraction with a deterministic mock provider by default
- Optional OpenAI-compatible LLM provider
- Persistent job and chat data
- Database configuration through `DATABASE_URL`
- SQS/SNS integration through environment configuration
- SQS worker for queue consumption
- Structured application logging with request IDs
- Dockerfile and starter CI workflow
- Fault-injection hooks for later troubleshooting exercises

## Course usage map

| Sprint | Reference application capability used |
| --- | --- |
| 1 | Not required |
| 2 | `/chat`, `/health`, Docker image, tests, application configuration |
| 3 | The Sprint 2 deployed application is the networking subject |
| 4 | Database persistence and SQS/SNS event publishing |
| 5 | Multi-step agent + LLM call + `/chat` for Langfuse instrumentation |
| 6 | `/metrics`, request/latency/error metrics |
| 7 | Multi-step request path for OpenTelemetry/Jaeger instrumentation |
| 8 | Application + database + messaging + IAM + ECS as one system |
| 9 | Logs, metrics, traces and asynchronous queue flow for incident diagnosis |
| 10 | Complete deployed system walkthrough |

## Run locally

### Option A: Python

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -e .
uvicorn app.main:app --reload
```

Open:

- http://localhost:8000/docs
- http://localhost:8000/health
- http://localhost:8000/metrics

### Option B: Docker Compose

```bash
docker compose up --build
```

The supplied Compose file runs JobScout AI with PostgreSQL.

## Test the API

```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Find me Python backend roles in Bangalore\"}"
```

For PowerShell, the same request can be sent with `Invoke-RestMethod`.

## Default behavior

The default LLM provider is `mock`. This keeps the application runnable without an external API key.

To use an OpenAI-compatible provider:

```text
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://your-provider.example/v1
LLM_API_KEY=your-key
LLM_MODEL=your-model
```

## Database

Default:

```text
DATABASE_URL=sqlite:///./data/jobscout.db
```

Docker Compose overrides this with PostgreSQL.

## Messaging

Messaging is disabled by default. Sprint 4 can enable it by supplying:

```text
MESSAGING_ENABLED=true
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_ENDPOINT_URL=http://localhost:4566
SQS_QUEUE_URL=<queue-url>
SNS_TOPIC_ARN=<topic-arn>
```

The application does not create the queue or topic automatically. This keeps provisioning as a separate cloud-service exercise.

## Worker

The worker consumes from the configured SQS queue:

```bash
python -m app.worker
```

## Fault injection

Normal behavior is:

```text
FAULT_MODE=none
```

Supported course-test hooks:

- `slow` - delay the `/chat` agent path
- `llm_error` - fail the LLM step
- `db_error` - fail persistence
- `queue_error` - fail event publishing

These hooks are disabled by default.

## Important design principle

The reference application provides the application-side capabilities the later demos need. Learners are not expected to develop JobScout AI itself as part of C12.
