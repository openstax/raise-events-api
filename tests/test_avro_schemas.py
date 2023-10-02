"""The tests in this file are expected to fail whenever we make changes that
modify the avro schema, and are here to help catch unexpected regressions when
models are not modified (e.g. when upgrading dependencies used to generate
avro schemas). We only expect / allow changes that maintain full transitive
compatibility (e.g. add or remove optional fields). Schema changes beyond this
require a new topic / version.
"""

import json
from eventsapi.models.avro import get_avro_schema
from eventsapi.models.api import ContentLoadedV1, ContentLoadFailedV1, \
    IbPsetProblemAttemptedV1, IbInputSubmittedV1
from aws_schema_registry.avro import AvroSchema


def test_content_loaded_v1_avro_schema():
    KafkaContentLoadedV1 = '{"type": "record", "name": "KafkaContentLoadedV1", "fields": [{"name": "user_uuid", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "course_id", "type": "long"}, {"name": "impression_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "source_scheme", "type": "string"}, {"name": "source_host", "type": "string"}, {"name": "source_path", "type": "string"}, {"name": "source_query", "type": "string"}, {"name": "timestamp", "type": "long"}, {"name": "content_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "variant", "type": "string"}], "namespace": "org.openstax.k12.raise.events"}'  # noqa: E501

    assert get_avro_schema(ContentLoadedV1) == \
        AvroSchema(json.loads(KafkaContentLoadedV1))


def test_content_load_failed_v1_avro_schema():
    KafkaContentLoadFailedV1 = '{"type": "record", "name": "KafkaContentLoadFailedV1", "fields": [{"name": "user_uuid", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "course_id", "type": "long"}, {"name": "impression_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "source_scheme", "type": "string"}, {"name": "source_host", "type": "string"}, {"name": "source_path", "type": "string"}, {"name": "source_query", "type": "string"}, {"name": "timestamp", "type": "long"}, {"name": "content_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "error", "type": ["null", "string"], "default": null}], "namespace": "org.openstax.k12.raise.events"}'  # noqa: E501

    assert get_avro_schema(ContentLoadFailedV1) == \
        AvroSchema(json.loads(KafkaContentLoadFailedV1))


def test_ib_pset_problem_attempted_v1_avro_schema():
    KafkaIbPsetProblemAttemptedV1 = '{"type": "record", "name": "KafkaIbPsetProblemAttemptedV1", "fields": [{"name": "user_uuid", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "course_id", "type": "long"}, {"name": "impression_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "source_scheme", "type": "string"}, {"name": "source_host", "type": "string"}, {"name": "source_path", "type": "string"}, {"name": "source_query", "type": "string"}, {"name": "timestamp", "type": "long"}, {"name": "content_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "variant", "type": "string"}, {"name": "problem_type", "type": "string"}, {"name": "response", "type": ["string", {"type": "array", "items": "string"}]}, {"name": "correct", "type": "boolean"}, {"name": "attempt", "type": "long"}, {"name": "final_attempt", "type": "boolean"}, {"name": "pset_content_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "pset_problem_content_id", "type": {"type": "string", "logicalType": "uuid"}}], "namespace": "org.openstax.k12.raise.events"}'  # noqa: E501

    assert get_avro_schema(IbPsetProblemAttemptedV1) == \
        AvroSchema(json.loads(KafkaIbPsetProblemAttemptedV1))


def test_ib_input_submitted_v1_avro_schema():
    KafkaIbInputSubmittedV1 = '{"type": "record", "name": "KafkaIbInputSubmittedV1", "fields": [{"name": "user_uuid", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "course_id", "type": "long"}, {"name": "impression_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "source_scheme", "type": "string"}, {"name": "source_host", "type": "string"}, {"name": "source_path", "type": "string"}, {"name": "source_query", "type": "string"}, {"name": "timestamp", "type": "long"}, {"name": "content_id", "type": {"type": "string", "logicalType": "uuid"}}, {"name": "variant", "type": "string"}, {"name": "response", "type": "string"}, {"name": "input_content_id", "type": {"type": "string", "logicalType": "uuid"}}], "namespace": "org.openstax.k12.raise.events"}'  # noqa: E501

    assert get_avro_schema(IbInputSubmittedV1) == \
        AvroSchema(json.loads(KafkaIbInputSubmittedV1))
