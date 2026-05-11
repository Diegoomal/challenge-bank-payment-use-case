import os

from fastapi import FastAPI
from observability.fastapi import configure_observability
from observability.logging import configure_logging

from adapters.api.routes import create_receipt_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.outbox_event_publisher import OutboxEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from adapters.messaging.saga_event_handler import SagaEventHandler
from adapters.persistence.sqlite_receipt_repository import SQLiteReceiptRepository
from adapters.receipt.in_memory_receipt_generator import InMemoryReceiptGenerator
from application.ports.event_publisher import EventPublisher
from application.ports.for_issuing_receipt import ForIssuingReceipt
from application.services.issue_receipt_service import IssueReceiptService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return OutboxEventPublisher()
    return InMemoryEventPublisher()


def configure_issue_receipt(
    database_path: str = "issue_receipt.db",
    rabbitmq_url: str | None = None,
) -> ForIssuingReceipt:
    repository = SQLiteReceiptRepository(database_path)
    receipt_generator = InMemoryReceiptGenerator()
    event_publisher = configure_event_publisher(rabbitmq_url)
    return IssueReceiptService(repository, receipt_generator, event_publisher)


def create_saga_event_handler(
    database_path: str = "issue_receipt.db",
    rabbitmq_url: str | None = None,
) -> SagaEventHandler:
    return SagaEventHandler(
        issue_receipt=configure_issue_receipt(database_path, rabbitmq_url)
    )


def create_saga_consumer(
    database_path: str = "issue_receipt.db",
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
    database_path: str = "issue_receipt.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Issue Receipt Service")
    configure_logging()
    configure_observability(app, os.getenv("OTEL_SERVICE_NAME", "Issue Receipt Service".lower().replace(" ", "_")))
    app.include_router(
        create_receipt_router(configure_issue_receipt(database_path, rabbitmq_url))
    )
    return app


configure_start_payment = configure_issue_receipt
