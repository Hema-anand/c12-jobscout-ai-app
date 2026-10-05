from datetime import datetime, timezone
import json

import boto3

from app.config import Settings


class MessagingPublisher:
    def __init__(self, settings: Settings):
        self.settings = settings
        kwargs = {
            "region_name": settings.aws_region,
            "aws_access_key_id": settings.aws_access_key_id,
            "aws_secret_access_key": settings.aws_secret_access_key,
        }
        if settings.aws_endpoint_url:
            kwargs["endpoint_url"] = settings.aws_endpoint_url
        self.sqs = boto3.client("sqs", **kwargs)
        self.sns = boto3.client("sns", **kwargs)

    def publish_search_completed(
        self,
        request_id: str,
        query: str,
        match_ids: list[int],
    ) -> dict[str, bool]:
        payload = {
            "event_type": "job_search.completed",
            "request_id": request_id,
            "query": query,
            "match_ids": match_ids,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        body = json.dumps(payload)

        results = {"sqs": False, "sns": False}

        if self.settings.sqs_queue_url:
            self.sqs.send_message(
                QueueUrl=self.settings.sqs_queue_url,
                MessageBody=body,
            )
            results["sqs"] = True

        if self.settings.sns_topic_arn:
            self.sns.publish(
                TopicArn=self.settings.sns_topic_arn,
                Message=body,
            )
            results["sns"] = True

        return results
