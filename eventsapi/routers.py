import logging
from typing import List
from fastapi import APIRouter, Depends
from eventsapi import kafka_producer
from eventsapi import auth
from eventsapi.models.avro import get_avro_schema
from eventsapi.models.api import \
    APIEvent, DetailMessage
from eventsapi.models.kafka import generate_kafka_model


logger = logging.getLogger(__name__)
v1_router = APIRouter()


@v1_router.post(
    "/events",
    status_code=201,
    response_model=DetailMessage)
async def create_events(
    events: List[APIEvent],
    user_uuid: str = Depends(auth.get_user_uuid),
    producer=Depends(kafka_producer.get_kafka_producer)
):
    logger.info("Received POST to /events")

    await producer.start()
    try:
        for event in events:
            kafka_event = generate_kafka_model(event, user_uuid).dict()
            schema = get_avro_schema(event.eventname)
            await producer.send(event.eventname, value=(kafka_event, schema))
    finally:
        await producer.stop()

    return {"detail": "Success!"}
