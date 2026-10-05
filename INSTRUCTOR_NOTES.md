# Instructor Notes

## Intent

JobScout AI is a ready-made reference application for C12. Learners should not spend sprint time building its core business functionality.

## Default local mode

- LLM provider: mock
- Database: SQLite
- Messaging: disabled
- Metrics: enabled
- Fault injection: disabled

This mode is intentionally self-contained and does not require a cloud account or external API key.

## Course progression

The application-side capabilities exist from the beginning. Sprint work is primarily about configuring and operating the surrounding infrastructure, security, cloud services and observability stack.

## Important boundary

Langfuse and OpenTelemetry/Jaeger integrations are not included in the base implementation. The application is structured so that those demos can instrument the existing agent steps without changing the application contract.
