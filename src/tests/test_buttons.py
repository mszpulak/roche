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


def test_button_on(clear_state):
    from src.main import app

    client = TestClient(app)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(off_message)

    body = ButtonsMessage(button=Buttons.ON)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(on_message)


def test_button_off(clear_state):
    from src.main import app

    client = TestClient(app)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(off_message)

    body = ButtonsMessage(button=Buttons.ON)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(on_message)

    body = ButtonsMessage(button=Buttons.OFF)
    response = client.post("/handle_button_push", json=dict(body))
    assert response.json() == dict(off_message)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(off_message)


def test_button_power(clear_state):
    from src.main import app

    client = TestClient(app)

    body = ButtonsMessage(button=Buttons.ON)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message)

    body = ButtonsMessage(button=Buttons.PLUS_POWER)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message) | {"power": 660}

    body = ButtonsMessage(button=Buttons.MINUS_POWER)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message) | {"power": 600}


def test_button_time(clear_state):
    from src.main import app

    client = TestClient(app)

    body = ButtonsMessage(button=Buttons.ON)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message)

    body = ButtonsMessage(button=Buttons.PLUS_TIME)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message) | {"time": 70}

    body = ButtonsMessage(button=Buttons.MINUS_TIME)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message) | {"time": 60}


def test_button_cancel(clear_state):
    from src.main import app

    client = TestClient(app)

    body = ButtonsMessage(button=Buttons.ON)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message)

    body = ButtonsMessage(button=Buttons.PLUS_POWER)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message) | {"power": 660}

    body = ButtonsMessage(button=Buttons.PLUS_TIME)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(on_message) | {"power": 660} | {"time": 70}

    body = ButtonsMessage(button=Buttons.CANCEL)
    response = client.post("/handle_button_push", json=dict(body))
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(off_message)
