import os

from fastapi import FastAPI
from observability.fastapi import configure_observability
from observability.logging import configure_logging

from adapters.api.routes import create_account_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.debit_completed_handler import DebitCompletedHandler
from adapters.messaging.outbox_event_publisher import OutboxEventPublisher
from adapters.messaging.rabbitmq_debit_completed_consumer import (
    RabbitMQDebitCompletedConsumer,
)
from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_crediting_account import ForCreditingAccount
from application.services.credit_account_service import CreditAccountService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return OutboxEventPublisher()
    return InMemoryEventPublisher()


def configure_credit_account(
    database_path: str = "credit_account.db",
    rabbitmq_url: str | None = None,
) -> ForCreditingAccount:
    repository = SQLiteAccountRepository(database_path)
    event_publisher = configure_event_publisher(rabbitmq_url)
    return CreditAccountService(repository, event_publisher)


def configure_debit_completed_handler(
    database_path: str = "credit_account.db",
    rabbitmq_url: str | None = None,
) -> DebitCompletedHandler:
    return DebitCompletedHandler(configure_credit_account(database_path, rabbitmq_url))


def create_debit_completed_consumer(
    database_path: str = "credit_account.db",
    rabbitmq_url: str | None = None,
) -> RabbitMQDebitCompletedConsumer:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to create the consumer")
    return RabbitMQDebitCompletedConsumer(
        rabbitmq_url=rabbitmq_url,
        handler=configure_debit_completed_handler(database_path, rabbitmq_url),
    )


def create_app(
    database_path: str = "credit_account.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Credit Account Service")
    configure_logging()
    configure_observability(
        app,
        os.getenv(
            "OTEL_SERVICE_NAME",
            "Credit Account Service".lower().replace(" ", "_"),
        ),
    )
    app.include_router(
        create_account_router(configure_credit_account(database_path, rabbitmq_url))
    )
    return app
