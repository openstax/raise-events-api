import uuid
from fastapi.testclient import TestClient
from typing import Dict, Callable


def test_post_events(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"},
                 {"kid": "kid2", "secret": "secret2"}]
    client = client_factory(auth_keys)
    body = [{
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_success_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "variant": "string"
    }]

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()


def test_post_two_different_kids(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"},
                 {"kid": "kid2", "secret": "secret2"}]
    client = client_factory(auth_keys)
    body = [{
         "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_success_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "variant": "string"
    }]

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid2", "secret2")
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()


def test_expired_jwt(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"},
                 {"kid": "kid2", "secret": "secret2"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(
        str(uuid.uuid4()), "kid1", "secret1", expired=True
    )
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 403
    assert response.json()['detail'] == 'Signature has expired.'


def test_invalid_kid_value_in_token(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"},
                 {"kid": "kid2", "secret": "secret2"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(
        str(uuid.uuid4()), "kid3", "secret1"
    )
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 403
    assert response.json()['detail'] == 'Invalid kid value in token'


def test_invalid_token(
    client_factory: Callable[[Dict], TestClient]
):
    client = client_factory({})

    auth_header = {
        "Authorization": "Bearer badtoken"
    }
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 403
    assert response.json()['detail'] == 'Error decoding token headers.'


def test_content_load_success_event(
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
        "eventname": "content_load_success_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "variant": "string"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()


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
        "eventname": "content_load_failure_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "details": "string"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()


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
        "eventname": "content_load_success_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "variant": "string"
    },
    {
         "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66af23",
        "source_uri": "string",
        "timestamp": 0,
        "eventname": "content_load_failure_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66af45",
        "details": "string"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()


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
        "eventname": "content_loaded_v1",
        "source_uri": "string",
        "timestamp": 0
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 422
    assert "detail" in response.json()