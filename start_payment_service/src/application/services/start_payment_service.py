from datetime import datetime, timezone

from application.ports.event_publisher import EventPublisher
from application.ports.for_starting_payment import ForStartingPayment
from application.ports.transaction_repository import TransactionRepository
from application.schemas import StartPaymentCommand, StartPaymentResult
from domain.events import PaymentStarted
from domain.transaction import Transaction


class StartPaymentService(ForStartingPayment):
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.event_publisher = event_publisher

    def start_payment(self, command: StartPaymentCommand) -> StartPaymentResult:
        transaction = Transaction.start(
            customer_id=command.customer_id,
            merchant_id=command.merchant_id,
            amount=command.amount,
            payment_method=command.payment_method,
        )

        self.transaction_repository.save(transaction)

        event = PaymentStarted(
            transaction_id=transaction.id,
            customer_id=transaction.customer_id,
            merchant_id=transaction.merchant_id,
            amount=transaction.amount,
            payment_method=transaction.payment_method,
            occurred_at=datetime.now(timezone.utc),
        )
        self.event_publisher.publish_payment_started(event)

        return StartPaymentResult(
            transaction_id=transaction.id,
            status=transaction.status,
            created_at=transaction.created_at,
        )
