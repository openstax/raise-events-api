import uuid
from fastapi.testclient import TestClient
from typing import Dict, Callable


def test_ib_pset_problem_attempted_v1_events(
    client_factory: Callable[[Dict], TestClient],
    admin_header_factory: Callable[[str], Dict]
):
    auth_keys = [{"kid": "kid1", "secret": "secret1"}]
    client = client_factory(auth_keys)

    auth_header = admin_header_factory(str(uuid.uuid4()), "kid1", "secret1")

    common_data = {
        "course_id": 0,
        "impression_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "source_uri": "http://localhost:8000",
        "timestamp": 0,
        "eventname": "ib_pset_problem_attempted_v1",
        "content_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "variant": "main",
        "pset_content_id": "5dac90ce-fdbc-4ea9-bfe3-fccd13fa9d12",
        "pset_problem_content_id": "743cb23f-527b-44b8-ac3b-39f88f8885b0"
    }

    body = [
        {
            **common_data,
            "problem_type": "input",
            "response": "some user input string",
            "correct": False,
            "attempt": 1,
            "final_attempt": False
        },
        {
            **common_data,
            "problem_type": "dropdown",
            "response": "selected input",
            "correct": False,
            "attempt": 1,
            "final_attempt": False
        },
        {
            **common_data,
            "problem_type": "multiselect",
            "response": ["selected input 1", "selected input 2"],
            "correct": False,
            "attempt": 1,
            "final_attempt": False
        },
        {
            **common_data,
            "problem_type": "multiplechoice",
            "response": "selected input",
            "correct": False,
            "attempt": 1,
            "final_attempt": False
        }
    ]
    response = client.post("/v1/events", json=body, headers=auth_header)
    assert response.status_code == 201
    assert response.json()['detail'] == 'Success!'
