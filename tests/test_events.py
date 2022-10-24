from fastapi.testclient import TestClient
import os


def test_post_events(client: TestClient):
    os.environ['SECRET'] = '[{"kid":"20221024", "secret":"d405ac2a54543423164171d1ad0b0c0bef90eeb936fb03d95f2fe8936c0f34ab"}]'
    response = client.post("/v1/events", headers={
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6IjIwMjIxMDI0In0.eyJzdWIiOiI0ODRiNmFkOS00ODA4LTRmYjQtYWYyZS1kOTVjMWY3MDRiZjQiLCJleHAiOjE2NjY3MjY2ODJ9.rbDn5WI7IxnstHy2zFaA0O0pAQm0asT3Rvibv7CAQlc"
    })
    assert response.status_code == 201
    assert "detail" in response.json()
