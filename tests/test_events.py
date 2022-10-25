import uuid
import uuid
from fastapi.testclient import TestClient
from typing import Dict, Callable


def test_post_events(
    client: TestClient, admin_header_factory: Callable[[str], Dict]
):
    auth_header = admin_header_factory(str(uuid.uuid4()))
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()