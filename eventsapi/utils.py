
from functools import cache
from unittest.mock import AsyncMock, Mock
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


async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER, acks='all')
    return producer


async def get_mock_producer():
    producer_mock = Mock()
    producer_mock.start = AsyncMock()
    producer_mock.send = AsyncMock()
    producer_mock.stop = AsyncMock()
    return producer_mock