import secrets
import uuid
import uuid
from fastapi.testclient import TestClient
from typing import Dict, Callable


def test_post_events(
    client_factory: Callable[[Dict], TestClient], admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{ "kid": "kid1", "secret":"secret1" },
                 { "kid": "kid2", "secret":"secret2" }]
    client = client_factory(auth_keys)
    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()


def test_post_two_different_kids(
    client_factory: Callable[[Dict], TestClient], admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{ "kid": "kid1", "secret":"secret1" },
                 { "kid": "kid2", "secret":"secret2" }]
    client = client_factory(auth_keys)
    
    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1" )
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid2", "secret2")
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 201
    assert "detail" in response.json()

def test_expired_jwt(
    client_factory: Callable[[Dict], TestClient], admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{ "kid": "kid1", "secret":"secret1" },
                 { "kid": "kid2", "secret":"secret2" }]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(str(uuid.uuid4()), "key1", "secret1", expired=True)
    response = client.post("/v1/events", headers=auth_header)
    assert response.status_code == 403
