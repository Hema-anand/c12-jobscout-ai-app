import json
import logging
import time

import boto3

from app.config import load_settings
from app.observability.logging import configure_logging


def main() -> None:
    configure_logging()
    logger = logging.getLogger("jobscout.worker")
    settings = load_settings()

    if not settings.messaging_enabled or not settings.sqs_queue_url:
        raise SystemExit(
            "Set MESSAGING_ENABLED=true and SQS_QUEUE_URL before starting the worker."
        )

    kwargs = {
        "region_name": settings.aws_region,
        "aws_access_key_id": settings.aws_access_key_id,
        "aws_secret_access_key": settings.aws_secret_access_key,
    }
    if settings.aws_endpoint_url:
        kwargs["endpoint_url"] = settings.aws_endpoint_url

    client = boto3.client("sqs", **kwargs)

    logger.info("worker_started queue=%s", settings.sqs_queue_url)

    while True:
        response = client.receive_message(
            QueueUrl=settings.sqs_queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10,
        )

        for message in response.get("Messages", []):
            body = message["Body"]
            payload = json.loads(body)
            logger.info(
                "event_received event_type=%s request_id=%s",
                payload.get("event_type"),
                payload.get("request_id"),
            )
            print(json.dumps(payload, indent=2))

            client.delete_message(
                QueueUrl=settings.sqs_queue_url,
                ReceiptHandle=message["ReceiptHandle"],
            )

        time.sleep(1)


if __name__ == "__main__":
    main()
