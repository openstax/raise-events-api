from typing import Optional
from urllib.parse import urlparse
from pydantic import BaseModel
from uuid import UUID
from eventsapi.models.api import \
    CONTENT_LOADED_V1, CONTENT_LOAD_FAILED_V1


class BaseKafkaEvent(BaseModel):
    user_uuid: UUID
    course_id: int
    impression_id: UUID
    source_scheme: str
    source_host: str
    source_path: str
    source_query: str
    timestamp: int


class KafkaContentLoadedV1(BaseKafkaEvent):
    content_id: UUID
    variant: str


class KafkaContentLoadFailedV1(BaseKafkaEvent):
    content_id: UUID
    error: Optional[str]


def generate_kafka_model(event, user_uuid):
    eventname = event.eventname
    url_parsed = urlparse(event.source_uri)
    fields = {
        "user_uuid": user_uuid,
        "course_id": event.course_id,
        "impression_id": event.impression_id,
        "source_scheme": url_parsed.scheme,
        "source_host": url_parsed.hostname,
        "source_path": url_parsed.path,
        "source_query": url_parsed.query,
        "timestamp": event.timestamp
    }

    if eventname == CONTENT_LOADED_V1:
        fields["content_id"] = event.content_id
        fields["variant"] = event.variant
        return KafkaContentLoadedV1(**fields)
    elif eventname == CONTENT_LOAD_FAILED_V1:
        fields["content_id"] = event.content_id
        fields["error"] = event.error
        return KafkaContentLoadFailedV1(**fields)
