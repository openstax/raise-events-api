from unittest.mock import AsyncMock, Mock
import pytest
import time
import json
from typing import Dict
from fastapi.testclient import TestClient
from starlette.config import environ
from jose import jwt, jwk
from eventsapi import utils

@pytest.fixture(scope="module")
def client_factory():
    def _client_generator(auth_keys):
        environ["AUTH_KEYS"] = json.dumps(auth_keys)
        from eventsapi.main import app
        app.dependency_overrides[utils.get_producer] = get_mock_producer
        return TestClient(app)
    return _client_generator


@pytest.fixture
def admin_header_factory() -> Dict:
    def _header_generator(uuid, kid, secret, expired=False):
        if not expired:
            expiry = time.time() + 60
        else:
            expiry = time.time() - 60
        payload = {
            "sub": uuid,
            "exp": expiry
        }
        key = hmac_key(secret)
        headers = hmac_headers(kid)
        token = jwt.encode(payload, key, headers=headers)
        return {"Authorization": f"Bearer {token}"}
    return _header_generator


def hmac_key(secret):
    return jwk.construct(secret, "HS256").to_dict()


def hmac_headers(kid):
    return {
        "kid": kid,
        "alg": "HS256",
        "typ": "JWT"
    }

def get_mock_producer():
    producer_mock = Mock()
    producer_mock.start = AsyncMock()
    producer_mock.send = AsyncMock()
    producer_mock.stop = AsyncMock()
    return producer_mock