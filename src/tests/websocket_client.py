import json

from websockets.sync.client import connect

with connect("ws://127.0.0.1:8001/ws_status") as websocket:
    message = json.loads(websocket.recv())
    print(f"Received: {message}")
    message = json.loads(websocket.recv())
    print(f"Received: {message}")
    message = json.loads(websocket.recv())
    print(f"Received: {message}")
