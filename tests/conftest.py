import pytest
import time
from typing import Dict
from typing import Generator
from fastapi.testclient import TestClient
from eventsapi.main import app
from starlette.config import environ
from jose import jwt, jwk

TEST_SECRET = "testsecret"
TEST_KID = "testkid"

client = TestClient(app)

@pytest.fixture(scope="module")
def client() -> Generator:
    environ["SECRET"] = f'[{{"kid":"{TEST_KID}", "secret":"{TEST_SECRET}"}}]'
    from eventsapi.main import app
    with TestClient(app) as c:
        yield c

@pytest.fixture
def hmac_key():
    return jwk.construct(TEST_SECRET, "HS256").to_dict()


@pytest.fixture
def hmac_headers():
    return {
        "kid": TEST_KID,
        "alg": "HS256",
        "typ": "JWT"
    }

@pytest.fixture
def admin_header_factory(hmac_key, hmac_headers) -> Dict:
    def _header_generator(uuid, expired=False):
        if not expired:
            expiry = time.time() + 60
        else: 
            expiry = time.time() - 60
        payload = {
            "sub": uuid,
            "exp": expiry
        }
        token = jwt.encode(payload, hmac_key, headers=hmac_headers)
        return {"Authorization": f"Bearer {token}"}
    return _header_generator