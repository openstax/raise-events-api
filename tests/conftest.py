from unittest.mock import AsyncMock, Mock
import pytest
import time
from typing import Dict
from fastapi.testclient import TestClient
from jose import jwt, jwk
from eventsapi import settings


@pytest.fixture(autouse=True)
def no_aiokafka_producer(monkeypatch):
    """Mock out AIOKafkaProducer for all tests."""
    monkeypatch.setattr("aiokafka.AIOKafkaProducer", get_mock_producer)


@pytest.fixture
def client_factory(monkeypatch):
    def _client_generator(auth_keys):
        monkeypatch.setattr(settings, "AUTH_KEYS", auth_keys)
        from eventsapi.main import app

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


def get_mock_producer(**kwargs):
    producer_mock = Mock()
    producer_mock.start = AsyncMock()
    producer_mock.send = AsyncMock()
    producer_mock.stop = AsyncMock()
    return producer_mock
