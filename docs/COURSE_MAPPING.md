# JobScout AI and C12 Sprint Mapping

This document explains what is already present in the reference application and what each sprint is expected to work on.

## Base application capabilities

The repository already contains the application-side functionality required by the course demos:

- `/chat` and a transparent multi-step agent workflow
- `/health` for service verification
- `/metrics` with request, latency, error and chat metrics
- A database layer that can use SQLite or PostgreSQL through `DATABASE_URL`
- SQS/SNS publisher support controlled by environment variables
- An SQS worker
- Structured logs and request IDs
- A Dockerfile and basic CI test workflow
- Configurable fault-injection hooks for instructor-led diagnosis

## What the sprints add or configure

### Sprint 2
The learner uses the existing application to practice IAM least privilege, container registry push, CI/CD extension and Floci ECS deployment. The application itself is not developed in this sprint.

### Sprint 3
The deployed application becomes the subject of the conceptual network design. No application feature is added.

### Sprint 4
The existing persistence and messaging capabilities are connected to the managed services created in the sprint.

### Sprint 5
The existing multi-step agent and LLM call are instrumented with Langfuse. Langfuse instrumentation is intentionally not bundled into the base application.

### Sprint 6
Prometheus is configured to scrape the existing `/metrics` endpoint and Grafana is used to visualize the metrics.

### Sprint 7
The existing multi-step request path is instrumented with OpenTelemetry and exported to Jaeger. OTel/Jaeger instrumentation is intentionally not bundled into the base application.

### Sprint 8
The previously configured IAM, ECS, database and messaging pieces are integrated into one running system.

### Sprint 9
Existing logs, metrics, traces and messaging flow are used to investigate a seeded incident.
