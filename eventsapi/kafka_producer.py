import boto3
from functools import partial
from aiokafka import AIOKafkaProducer
from aws_schema_registry import SchemaRegistryClient
from kafka.serializer import Serializer
from aws_schema_registry import DataAndSchema
from aws_schema_registry.adapter.kafka import KafkaSerializer
from eventsapi.settings import \
    GLUE_REGISTRY_NAME, AWS_REGION, \
    KAFKA_BOOTSTRAP_BROKERS


class KafkaAvroSerializer(Serializer):
    def serialize(self, topic: str, data_and_schema: DataAndSchema):
        data, schema = data_and_schema
        value = schema.write(data)
        return value


def build_callable_serializer(serializer):
    def _serialize_data(data_schema_topic, serializer):
        data, schema, topic = data_schema_topic
        return serializer.serialize(topic, (data, schema))
    return partial(_serialize_data, serializer=serializer)


def get_kafka_producer():
    if (GLUE_REGISTRY_NAME):
        serializer = get_kafka_glue_serializer()
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_BROKERS,
            security_protocol="SSL",
            value_serializer=build_callable_serializer(serializer),
            acks='all'
        )
        return producer
    else:
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_BROKERS,
            value_serializer=build_callable_serializer(KafkaAvroSerializer()),
            acks='all'
        )
        return producer


def get_kafka_glue_serializer():
    glue_client = boto3.client('glue', region_name=AWS_REGION)
    client = SchemaRegistryClient(
        glue_client,
        registry_name=GLUE_REGISTRY_NAME
    )
    return KafkaSerializer(client, compatibility_mode='FULL_ALL')


aiokafka_producer = get_kafka_producer()
