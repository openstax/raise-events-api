import logging
from typing import List
from fastapi import APIRouter, Depends
from eventsapi import auth
from eventsapi.models.avro import get_avro_schema
from eventsapi.models.api import \
    APIEvent, DetailMessage
from eventsapi.models.kafka import generate_kafka_model
from eventsapi.kafka_producer import aiokafka_producer


logger = logging.getLogger(__name__)
v1_router = APIRouter()


@v1_router.post(
    "/events",
    status_code=201,
    response_model=DetailMessage)
async def create_events(
    events: List[APIEvent],
    user_uuid: str = Depends(auth.get_user_uuid)
):
    logger.info(f"Received POST to /events with {len(events)} item(s)")

    for event in events:
        kafka_event = generate_kafka_model(event, user_uuid).model_dump()
        schema = get_avro_schema(type(event))
        await aiokafka_producer.send(
            event.eventname,
            value=(kafka_event, schema, event.eventname)
        )

    return {"detail": "Success!"}
