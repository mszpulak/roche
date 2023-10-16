from websockets.sync.client import connect
import json

with connect("ws://127.0.0.1:8001/ws_status") as websocket:
    message = json.loads(websocket.recv())
    print(f"Received: {message}")
    message = json.loads(websocket.recv())
    print(f"Received: {message}")
    message = json.loads(websocket.recv())
    print(f"Received: {message}")
