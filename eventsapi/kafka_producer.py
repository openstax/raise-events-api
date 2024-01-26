import boto3
from aiokafka import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context
from aws_schema_registry import SchemaRegistryClient
from aws_schema_registry import DataAndSchema
from aws_schema_registry.serde import KafkaSerializer
from eventsapi.settings import \
    GLUE_REGISTRY_NAME, GLUE_AWS_REGION, KAFKA_BOOTSTRAP_BROKERS, \
    KAFKA_SASL_USERNAME, KAFKA_SASL_PASSWORD


class KafkaAvroSerializer:
    def serialize(self, topic: str, data_and_schema: DataAndSchema):
        data, schema = data_and_schema
        value = schema.write(data)
        return value


def build_callable_serializer(serializer):
    def _serialize_data(data_schema_topic):
        data, schema, topic = data_schema_topic
        return serializer.serialize(topic, (data, schema))
    return _serialize_data


def get_kafka_producer():
    if (GLUE_REGISTRY_NAME):
        serializer = get_kafka_glue_serializer()
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_BROKERS,
            value_serializer=build_callable_serializer(serializer),
            acks='all',
            security_protocol="SASL_SSL",
            ssl_context=create_ssl_context(),
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username=KAFKA_SASL_USERNAME,
            sasl_plain_password=KAFKA_SASL_PASSWORD
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
    glue_client = boto3.client('glue', region_name=GLUE_AWS_REGION)
    client = SchemaRegistryClient(
        glue_client,
        registry_name=GLUE_REGISTRY_NAME
    )
    return KafkaSerializer(client, compatibility_mode='FULL_ALL')


aiokafka_producer = get_kafka_producer()
