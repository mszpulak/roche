import httpx

r = httpx.get("http://localhost:8001/status")
print(r.json())


r = httpx.post("http://localhost:8001/handle_button_push", json={"button": "ON"})
print(r.json())

r = httpx.post(
    "http://localhost:8001/handle_button_push", json={"button": "PLUS_POWER"}
)
print(r.json())

r = httpx.post(
    "http://localhost:8001/handle_button_push", json={"button": "MINUS_TIME"}
)
print(r.json())

r = httpx.post("http://localhost:8001/handle_button_push", json={"button": "OFF"})
print(r.json())
