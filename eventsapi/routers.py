import logging
from typing import List
from fastapi import APIRouter, Depends
from urllib.parse import urlparse
from eventsapi import utils
from eventsapi import auth
from eventsapi.models import \
    Event, DetailMessage, \
    KafkaContentLoadFailedV1, KafkaContentLoadedV1, \
    CONTENT_LOADED_V1, CONTENT_LOAD_FAILED_V1


logger = logging.getLogger(__name__)
v1_router = APIRouter()


@v1_router.post(
    "/events",
    status_code=201,
    response_model=DetailMessage)
async def create_events(
    events: List[Event],
    user_uuid: str = Depends(auth.get_user_uuid),
    producer=Depends(utils.get_producer)
):
    logger.info("Received POST to /events")

    await producer.start()

    for event in events:
        k_event = generate_kafka_model(event, user_uuid).dict()
        schema = utils.get_schema(event.eventname)
        await producer.send(event.eventname, value=(k_event, schema))

    await producer.stop()

    return {"detail": "Success!"}


def generate_kafka_model(event, user_uuid):
    eventname = event.eventname
    url_parsed = urlparse(event.source_uri)
    fields = {
        "user_uuid": user_uuid,
        "course_id": event.course_id,
        "impression_id": str(event.impression_id),
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
