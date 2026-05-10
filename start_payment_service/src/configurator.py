from fastapi import FastAPI

from adapters.api.routes import create_payment_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.persistence.sqlite_transaction_repository import (
    SQLiteTransactionRepository,
)
from application.ports.for_starting_payment import ForStartingPayment
from application.services.start_payment_service import StartPaymentService


def configure_start_payment(
    database_path: str = "start_payment.db",
) -> ForStartingPayment:
    repository = SQLiteTransactionRepository(database_path)
    event_publisher = InMemoryEventPublisher()
    return StartPaymentService(repository, event_publisher)


def create_app(database_path: str = "start_payment.db") -> FastAPI:
    app = FastAPI(title="Start Payment Service")
    app.include_router(create_payment_router(configure_start_payment(database_path)))
    return app
