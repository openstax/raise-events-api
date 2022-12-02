import json
from functools import cache
import py_avro_schema as pas
from aws_schema_registry.avro import AvroSchema
from eventsapi.models.kafka import \
    KafkaContentLoadedV1, KafkaContentLoadFailedV1
from eventsapi.models.api import \
    CONTENT_LOADED_V1, CONTENT_LOAD_FAILED_V1

AVRO_NAMESPACE = "org.openstax.k12.raise.events"


@cache
def get_avro_schema(eventname):

    if eventname == CONTENT_LOADED_V1:
        kafka_event_cls = KafkaContentLoadedV1
    elif eventname == CONTENT_LOAD_FAILED_V1:
        kafka_event_cls = KafkaContentLoadFailedV1

    schema_json = pas.generate(
        kafka_event_cls,
        namespace=AVRO_NAMESPACE
    )

    return AvroSchema(json.loads(schema_json))
