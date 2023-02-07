import json
from functools import cache
import py_avro_schema as pas
from aws_schema_registry.avro import AvroSchema
from eventsapi.models.kafka import API_TO_KAFKA_MODEL_MAP

AVRO_NAMESPACE = "org.openstax.k12.raise.events"


@cache
def get_avro_schema(event_type):

    kafka_event_cls = API_TO_KAFKA_MODEL_MAP[event_type]

    schema_json = pas.generate(
        kafka_event_cls,
        namespace=AVRO_NAMESPACE
    )

    return AvroSchema(json.loads(schema_json))
