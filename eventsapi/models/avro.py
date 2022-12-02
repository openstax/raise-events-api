import json
from functools import cache
import py_avro_schema as pas
from aws_schema_registry.avro import AvroSchema
from eventsapi.models.kafka import \
    KafkaContentLoadedV1, KafkaContentLoadFailedV1
from eventsapi.models.api import \
    ContentLoadedV1, ContentLoadFailedV1

AVRO_NAMESPACE = "org.openstax.k12.raise.events"


@cache
def get_avro_schema(event_type):

    if event_type == ContentLoadedV1:
        kafka_event_cls = KafkaContentLoadedV1
    elif event_type == ContentLoadFailedV1:
        kafka_event_cls = KafkaContentLoadFailedV1

    schema_json = pas.generate(
        kafka_event_cls,
        namespace=AVRO_NAMESPACE
    )

    return AvroSchema(json.loads(schema_json))
