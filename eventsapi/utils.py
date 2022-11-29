
from asyncio import Future
from functools import cache
from unittest.mock import AsyncMock
import py_avro_schema as pas
from aiokafka import AIOKafkaProducer
from eventsapi.models import KafkaContentLoadedV1, KafkaContentLoadFailedV1, CONTENT_LOADED_V1, CONTENT_LOAD_FAILED_V1
from fastavro import parse_schema
import json

KAFKA_SERVER = "kafka:29092"


@cache
def get_schema(eventname):
    
    if eventname == CONTENT_LOADED_V1:
        schema_json = pas.generate(
            KafkaContentLoadedV1,
            namespace="org.openstax.k12.raise.events"
        )
        return parse_schema(json.loads(schema_json))
    elif eventname == CONTENT_LOAD_FAILED_V1:
        schema_json = pas.generate(
            KafkaContentLoadFailedV1,
            namespace="org.openstax.k12.raise.events"
        )
        return parse_schema(json.loads(schema_json))


@cache 
def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER, acks='all')
    return producer

@cache 
def get_mock_producer():
    producer_mock = AsyncMock()
    producer_mock.send.return_value = "ack"
    producer_mock.start.return_value = "ack"
    return producer_mock