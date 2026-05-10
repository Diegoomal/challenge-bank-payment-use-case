# Reverse Payment Service Setup

## Run The Service

```bash
make run
```

Manual run:

```bash
PYTHONPATH=src uvicorn main:app --reload --port 8004
```

## Run Consumer

```bash
PYTHONPATH=src python src/consumer.py
```

## Docker

```bash
docker compose up -d --build reverse_payment_service reverse_payment_consumer
```

## Run Tests

```bash
make test
make lint
make check
```
