import uuid
from fastapi.testclient import TestClient
from typing import Dict, Callable


def test_content_load_failure_event(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    body = [{
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_failed_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "error": "string"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert response.json()['detail'] == 'Success!'


def test_content_load_failure_event_optional_error_field(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    body = [{
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_failed_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert response.json()['detail'] == 'Success!'


def test_multiple_events(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    body = [{
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_failed_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "error": "string"
    }, {
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_failed_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "error": "string"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert response.json()['detail'] == 'Success!'


def test_invalid_event_body(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    body = [{
        "course_id": "abc",
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "content_id": "string",
        "eventname": "content_load_failed_v1",
        "source_uri": "string",
        "timestamp": 0,
        "error": "string"

    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 422
