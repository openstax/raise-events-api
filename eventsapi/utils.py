
from functools import cache
import io
import py_avro_schema as pas
from aiokafka import AIOKafkaProducer
from eventsapi.models import KafkaContentLoadedV1, KafkaContentLoadFailedV1, CONTENT_LOADED_V1, CONTENT_LOAD_FAILED_V1
from aws_schema_registry.avro import AvroSchema
from aws_schema_registry import SchemaRegistryClient, DataAndSchema
from kafka.serializer import Serializer
from kafka.record.legacy_records import LegacyRecordBatchBuilder
from kafka.errors import MessageSizeTooLargeError
from aws_schema_registry.adapter.kafka import KafkaSerializer
from fastavro import writer
from eventsapi.settings import GLUE_REGISTRY_NAME, AWS_REGION, KAFKA_BOOTSTRAP_BROKERS
import json
import boto3


@cache
def get_schema(eventname):

    if eventname == CONTENT_LOADED_V1:
        schema_json = pas.generate(
            KafkaContentLoadedV1,
            namespace="org.openstax.k12.raise.events"
        )
        return AvroSchema(json.loads(schema_json))
    elif eventname == CONTENT_LOAD_FAILED_V1:
        schema_json = pas.generate(
            KafkaContentLoadFailedV1,
            namespace="org.openstax.k12.raise.events"
        )
        return AvroSchema(json.loads(schema_json))


class KafkaAvroSerializer(Serializer):
    def serialize(self, topic: str, data_and_schema: DataAndSchema):
        data, schema = data_and_schema
        value = schema.write(data)
        return value


class CustomKafkaProducer(AIOKafkaProducer):
    """A custom Kafka client based on AIOKafkaProducer which overrides
    some of the serialization logic to support value serializers that are
    either callables or Serializer types (essentially incorporating some logic
    from kafka-python's KafkaProducer so there is feature parity)
    """
    def _serialize(self, topic, key, value):
        if self._key_serializer:
            serialized_key = self._key_serializer(key)
        else:
            serialized_key = key
        if self._value_serializer:
            if isinstance(self._value_serializer, Serializer):
                serialized_value = \
                    self._value_serializer.serialize(topic, value)
            else:
                serialized_value = self._value_serializer(value)
        else:
            serialized_value = value

        message_size = LegacyRecordBatchBuilder.record_overhead(
            self._producer_magic)
        if serialized_key is not None:
            message_size += len(serialized_key)
        if serialized_value is not None:
            message_size += len(serialized_value)
        if message_size > self._max_request_size:
            raise MessageSizeTooLargeError(
                "The message is %d bytes when serialized which is larger than"
                " the maximum request size you have configured with the"
                " max_request_size configuration" % message_size)

        return serialized_key, serialized_value

async def get_producer():
    if (not GLUE_REGISTRY_NAME):
        producer = CustomKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_BROKERS,
            value_serializer=KafkaAvroSerializer(),
            acks='all'
        )
        return producer
    else:
        serializer = get_glue_serializer()
        producer = CustomKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_BROKERS,
            security_protocol="SSL",
            value_serializer=serializer,
            acks='all'
        )
        return producer


async def get_glue_serializer():
    glue_client = boto3.client('glue', region_name=AWS_REGION)
    client = SchemaRegistryClient(
        glue_client,
        registry_name=GLUE_REGISTRY_NAME
    )
    return KafkaSerializer(client, compatibility_mode='FULL_ALL')