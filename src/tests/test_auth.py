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
token = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiw
ibmFtZSI6Ik1hcmNpbiBTenB1bGFrIiwiaWF0IjoxNjk3Mjc4OTE1LCJhdWQiOiJBWlVSRV9CQUN
LRU5EX0NMSUVOVF9JRCIsImlzcyI6IkFaVVJFX0JBQ0tFTkRfVEVOQU5UIiwiZXhwIjoxNzI4OTA
xMzE1fQ.GWkmndWeRXUR80p0uBRwC3iaK2kjZZ-Hmv67x5SpXUs"""

"""
{
  "sub": "1234567890",
  "name": "Marcin Szpulak",
  "iat": 1697278915,
  "aud": "AZURE_BACKEND_CLIENT_ID",
  "iss": "AZURE_BACKEND_TENANT",
  "exp": 1728901315
}
"""


def test_auth(clear_state):
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

    response = client.post(
        "/cancel", headers={"Authorization": "Bearer {}".format(token)}
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json() == dict(off_message)


def test_auth_error(clear_state):
    from src.main import app

    client = TestClient(app)

    response = client.get("/status")
    print(response.json())
    assert response.json() == dict(off_message)

    response = client.post("/cancel")
    print(response.json())

    assert response.status_code == 403
