from fastapi.testclient import TestClient


def test_websocket():
    from src.main import app

    client = TestClient(app)

    with client.websocket_connect("/ws_status") as websocket:
        message = websocket.receive_json()
        assert message == {"state": "off", "power": 600, "time": 60}
        print(message)
