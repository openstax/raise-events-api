from typing import Optional, Union, List
from urllib.parse import urlparse
from pydantic import BaseModel
from uuid import UUID
from eventsapi.models.api import \
    ContentLoadedV1, ContentLoadFailedV1, IbPsetProblemAttemptedV1


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


class KafkaIbPsetProblemAttemptedV1(BaseKafkaEvent):
    content_id: UUID
    variant: str
    problem_type: str
    response: Union[str, List[str]]
    correct: bool
    attempt: int
    final_attempt: bool
    pset_content_id: UUID
    pset_problem_content_id: UUID


def generate_kafka_model(event, user_uuid):
    event_type = type(event)
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

    if event_type == ContentLoadedV1:
        for value in ["content_id", "variant"]:
            fields[value] = getattr(event, value)
        return KafkaContentLoadedV1(**fields)
    elif event_type == ContentLoadFailedV1:
        for value in ["content_id", "error"]:
            fields[value] = getattr(event, value)
        return KafkaContentLoadFailedV1(**fields)
    elif event_type == IbPsetProblemAttemptedV1:
        for value in [
            "content_id", "variant", "problem_type", "response",
            "correct", "attempt", "final_attempt", "pset_content_id",
            "pset_problem_content_id"
        ]:
            fields[value] = getattr(event, value)
        return KafkaIbPsetProblemAttemptedV1(**fields)
