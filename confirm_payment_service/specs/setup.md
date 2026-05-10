# Confirm Payment Service Setup

## Requirements

The project uses Python 3.10 and dependencies listed in `requirements.txt`.

## Conda Environment

```bash
conda env create -n confirm-payment-service-env -f env.yml
conda activate confirm-payment-service-env
```

## Run The Service

```bash
make run
```

Manual run:

```bash
PYTHONPATH=src uvicorn main:app --reload --port 8003
```

## Run Consumer

```bash
PYTHONPATH=src python src/consumer.py
```

## Docker

From the repository root:

```bash
docker compose up -d --build confirm_payment_service confirm_payment_consumer
```

## Run Tests

```bash
make test
make lint
make check
```
