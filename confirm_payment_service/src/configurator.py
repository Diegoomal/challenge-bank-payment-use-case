import os

from fastapi import FastAPI

from adapters.api.routes import create_payment_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from adapters.messaging.saga_event_handler import SagaEventHandler
from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from application.ports.event_publisher import EventPublisher
from application.ports.for_confirming_payment import ForConfirmingPayment
from application.services.confirm_payment_service import ConfirmPaymentService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return RabbitMQEventPublisher(rabbitmq_url)
    return InMemoryEventPublisher()


def configure_confirm_payment(
    database_path: str = "confirm_payment.db",
    rabbitmq_url: str | None = None,
) -> ForConfirmingPayment:
    repository = SQLiteTransactionRepository(database_path)
    event_publisher = configure_event_publisher(rabbitmq_url)
    return ConfirmPaymentService(repository, event_publisher)


def create_saga_event_handler(
    database_path: str = "confirm_payment.db",
    rabbitmq_url: str | None = None,
) -> SagaEventHandler:
    repository = SQLiteTransactionRepository(database_path)
    return SagaEventHandler(
        transaction_repository=repository,
        confirm_payment=ConfirmPaymentService(
            repository,
            configure_event_publisher(rabbitmq_url),
        ),
    )


def create_saga_consumer(
    database_path: str = "confirm_payment.db",
    rabbitmq_url: str | None = None,
) -> RabbitMQSagaConsumer:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to create the consumer")
    return RabbitMQSagaConsumer(
        rabbitmq_url=rabbitmq_url,
        handler=create_saga_event_handler(database_path, rabbitmq_url),
    )


def create_app(
    database_path: str = "confirm_payment.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Confirm Payment Service")
    app.include_router(
        create_payment_router(configure_confirm_payment(database_path, rabbitmq_url))
    )
    return app
