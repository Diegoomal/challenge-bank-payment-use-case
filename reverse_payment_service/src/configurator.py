import os

from fastapi import FastAPI
from observability.fastapi import configure_observability
from observability.logging import configure_logging

from adapters.api.routes import create_payment_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.outbox_event_publisher import OutboxEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from adapters.messaging.saga_event_handler import SagaEventHandler
from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from application.ports.event_publisher import EventPublisher
from application.ports.for_reversing_payment import ForReversingPayment
from application.services.reverse_payment_service import ReversePaymentService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return OutboxEventPublisher()
    return InMemoryEventPublisher()


def configure_reverse_payment(
    database_path: str = "reverse_payment.db",
    rabbitmq_url: str | None = None,
) -> ForReversingPayment:
    repository = SQLiteTransactionRepository(database_path)
    event_publisher = configure_event_publisher(rabbitmq_url)
    return ReversePaymentService(repository, event_publisher)


def create_saga_event_handler(
    database_path: str = "reverse_payment.db",
    rabbitmq_url: str | None = None,
) -> SagaEventHandler:
    repository = SQLiteTransactionRepository(database_path)
    return SagaEventHandler(
        transaction_repository=repository,
        reverse_payment=ReversePaymentService(
            repository,
            configure_event_publisher(rabbitmq_url),
        ),
    )


def create_saga_consumer(
    database_path: str = "reverse_payment.db",
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
    database_path: str = "reverse_payment.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Reverse Payment Service")
    configure_logging()
    configure_observability(app, os.getenv("OTEL_SERVICE_NAME", "Reverse Payment Service".lower().replace(" ", "_")))
    app.include_router(
        create_payment_router(configure_reverse_payment(database_path, rabbitmq_url))
    )
    return app
