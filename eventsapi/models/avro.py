import json
from functools import cache
import py_avro_schema as pas
from aws_schema_registry.avro import AvroSchema
from eventsapi.models.kafka import \
    KafkaContentLoadedV1, KafkaContentLoadFailedV1, \
    KafkaIbPsetProblemAttemptedV1
from eventsapi.models.api import \
    ContentLoadedV1, ContentLoadFailedV1, IbPsetProblemAttemptedV1

AVRO_NAMESPACE = "org.openstax.k12.raise.events"

API_TO_KAFKA_MODEL_MAP = {
    ContentLoadedV1: KafkaContentLoadedV1,
    ContentLoadFailedV1: KafkaContentLoadFailedV1,
    IbPsetProblemAttemptedV1: KafkaIbPsetProblemAttemptedV1
}


@cache
def get_avro_schema(event_type):

    kafka_event_cls = API_TO_KAFKA_MODEL_MAP[event_type]

    schema_json = pas.generate(
        kafka_event_cls,
        namespace=AVRO_NAMESPACE
    )

    return AvroSchema(json.loads(schema_json))
