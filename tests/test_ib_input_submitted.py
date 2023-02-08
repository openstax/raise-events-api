import uuid
from fastapi.testclient import TestClient
from typing import Dict, Callable


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
        "source_uri": "https://localhost:8000",
        "timestamp": 0,
        "eventname": "ib_input_submitted_v1",
        "content_id": "55585f64-5717-4562-b3fc-2c963f66afa6",
        "variant": "main",
        "response": "ASDF",
        "input_content_id": "88885f64-5717-4562-b3fc-2c963f66afa6"
    }, {
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "https://localhost:8000",
        "timestamp": 0,
        "eventname": "ib_input_submitted_v1",
        "content_id": "55585f64-5717-4562-b3fc-2c963f66afa6",
        "variant": "second",
        "response": "100",
        "input_content_id": "99995f64-5717-4562-b3fc-2c963f66afa6"
    }]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert response.json()['detail'] == 'Success!'
