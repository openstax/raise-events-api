from fastapi.testclient import TestClient


def test_post_events(client: TestClient):
    response = client.post("/v1/events", json={})
    assert response.status_code == 201
    assert "detail" in response.json()
