from typing import Optional, Union, List
from urllib.parse import urlparse
from pydantic import BaseModel
from uuid import UUID
from eventsapi.models.api import \
    ContentLoadedV1, ContentLoadFailedV1, \
    IbPsetProblemAttemptedV1, IbInputSubmittedV1


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


class KafkaIbInputSubmittedV1(BaseKafkaEvent):
    content_id: UUID
    variant: str
    response: str
    input_content_id: UUID


API_TO_KAFKA_MODEL_MAP = {
    ContentLoadedV1: KafkaContentLoadedV1,
    ContentLoadFailedV1: KafkaContentLoadFailedV1,
    IbPsetProblemAttemptedV1: KafkaIbPsetProblemAttemptedV1,
    IbInputSubmittedV1: KafkaIbInputSubmittedV1
}


API_TO_KAFKA_SHARED_FIELDS_MAP = {
    ContentLoadedV1: ["content_id", "variant"],
    ContentLoadFailedV1: ["content_id", "error"],
    IbPsetProblemAttemptedV1: [
        "content_id", "variant", "problem_type", "response",
        "correct", "attempt", "final_attempt", "pset_content_id",
        "pset_problem_content_id"
    ],
    IbInputSubmittedV1: [
        "content_id", "variant", "response", "input_content_id"
    ]
}


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

    for value in API_TO_KAFKA_SHARED_FIELDS_MAP[event_type]:
        fields[value] = getattr(event, value)

    return API_TO_KAFKA_MODEL_MAP[event_type](**fields)
