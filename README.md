# roche

## Setting up dev enviroment

How to install poetry: https://python-poetry.org/docs/#installing-with-the-official-installer
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Prepare your local setup.
Change direcotry to src folder
```bash
cd src
poetry install
```

Entering local virtualenv:
```bash
poetry shell
```

Install pre-commit hook (from above directory):
```bash
cd ..
pre-commit install
```
## Running tests:

```bash
pytest src/tests/
```

## Running SW stack in docker compose:

```bash
docker compose build
docker compose up
```

checking redis cluster status if connectionfails
```bash
docker exec -it roche-redis-node-5-1 /bin/bash
redis-cli -c CLUSTER INFO
```

## Start server manually
check endpoints using script
```bash
uvicorn --host 0.0.0.0 --port 8001 src.main:app
python src/tests/web_client.py
```

## Connect to HTML frontpage
check endpoints using script
```bash
http://127.0.0.1:8001/
```

## Connect to HTML frontpage via reverse proxy
check endpoints using script
```bash
curl http://127.0.0.1:3000
```
