from fastapi.testclient import TestClient
from src.schema import StatusMessage, ButtonsMessage, Buttons

off_message = StatusMessage(
    power=600,
    time=60,
    state="off",
)

on_message = StatusMessage(
    power=600,
    time=60,
    state="on",
)


def test_button_cancel(clear_state):
    from src.main import app

    client = TestClient(app)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(off_message)

    body = ButtonsMessage(button=Buttons.OFF)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 400
