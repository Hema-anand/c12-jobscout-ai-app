# JobScout AI Architecture

The application is intentionally small. The purpose is to provide a stable system on which C12 cloud, deployment and observability demos can operate.

```text
Client
  |
  +--> POST /chat
  |        |
  |        +--> parse_request
  |        +--> retrieve_jobs --> Database
  |        +--> rank_jobs
  |        +--> generate_response --> LLM provider
  |        |
  |        +--> persist chat session --> Database
  |        +--> publish event --> SQS / SNS
  |
  +--> GET /health
  |
  +--> GET /metrics --> Prometheus

SQS --> app.worker
```

## Instrumentation points

The agent steps are intentionally explicit:

- `parse_request`
- `retrieve_jobs`
- `rank_jobs`
- `generate_response`

These are the natural points for the later Langfuse and OpenTelemetry demos.

## Configuration boundaries

External systems are configured through environment variables rather than embedded in application code:

- `DATABASE_URL`
- `LLM_*`
- `AWS_*`
- `SQS_QUEUE_URL`
- `SNS_TOPIC_ARN`

This makes the same application usable locally, with PostgreSQL, and with Floci-managed services without changing business logic.
