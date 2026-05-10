import os

from fastapi import FastAPI
from observability.fastapi import configure_observability
from observability.logging import configure_logging

from adapters.api.routes import create_account_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.payment_started_handler import PaymentStartedHandler
from adapters.messaging.outbox_event_publisher import OutboxEventPublisher
from adapters.messaging.rabbitmq_payment_started_consumer import (
    RabbitMQPaymentStartedConsumer,
)
from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_debiting_account import ForDebitingAccount
from application.services.debit_account_service import DebitAccountService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return OutboxEventPublisher()
    return InMemoryEventPublisher()


def configure_debit_account(
    database_path: str = "debit_account.db",
    rabbitmq_url: str | None = None,
) -> ForDebitingAccount:
    repository = SQLiteAccountRepository(database_path)
    event_publisher = configure_event_publisher(rabbitmq_url)
    return DebitAccountService(repository, event_publisher)


def configure_payment_started_handler(
    database_path: str = "debit_account.db",
    rabbitmq_url: str | None = None,
) -> PaymentStartedHandler:
    return PaymentStartedHandler(configure_debit_account(database_path, rabbitmq_url))


def create_payment_started_consumer(
    database_path: str = "debit_account.db",
    rabbitmq_url: str | None = None,
) -> RabbitMQPaymentStartedConsumer:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to create the consumer")
    return RabbitMQPaymentStartedConsumer(
        rabbitmq_url=rabbitmq_url,
        handler=configure_payment_started_handler(database_path, rabbitmq_url),
    )


def create_app(
    database_path: str = "debit_account.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Debit Account Service")
    configure_logging()
    configure_observability(app, os.getenv("OTEL_SERVICE_NAME", "Debit Account Service".lower().replace(" ", "_")))
    app.include_router(
        create_account_router(configure_debit_account(database_path, rabbitmq_url))
    )
    return app
