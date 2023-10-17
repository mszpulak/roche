from fastapi.testclient import TestClient

from src.schema import StatusMessage

expected_message = StatusMessage(
    power=600,
    time=60,
    state="off",
)


def test_status_off(clear_state):
    from src.main import app

    client = TestClient(app)
    response = client.get("/status")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == dict(expected_message)
