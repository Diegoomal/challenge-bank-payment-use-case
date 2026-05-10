import os

from fastapi import FastAPI

from adapters.api.routes import create_payment_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.outbox_event_publisher import OutboxEventPublisher
from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from application.ports.event_publisher import EventPublisher
from application.ports.for_starting_payment import ForStartingPayment
from application.services.start_payment_service import StartPaymentService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return OutboxEventPublisher()
    return InMemoryEventPublisher()


def configure_start_payment(
    database_path: str = "start_payment.db",
    rabbitmq_url: str | None = None,
) -> ForStartingPayment:
    repository = SQLiteTransactionRepository(database_path)
    event_publisher = configure_event_publisher(rabbitmq_url)
    return StartPaymentService(repository, event_publisher)


def create_app(
    database_path: str = "start_payment.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Start Payment Service")
    app.include_router(
        create_payment_router(configure_start_payment(database_path, rabbitmq_url))
    )
    return app
