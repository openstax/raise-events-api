
from functools import cache
import py_avro_schema as pas
from eventsapi.models import KafkaContentLoadedV1, KafkaContentLoadFailedV1, CONTENT_LOADED_V1, CONTENT_LOAD_FAILED_V1
from fastavro import parse_schema
import json

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