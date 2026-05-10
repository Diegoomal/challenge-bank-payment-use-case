from application.ports.event_publisher import EventPublisher
from application.ports.for_confirming_payment import ForConfirmingPayment
from application.ports.transaction_repository import TransactionRepository
from application.schemas import ConfirmPaymentCommand, ConfirmPaymentResult
from domain.events import PaymentConfirmed


class ConfirmPaymentService(ForConfirmingPayment):
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.event_publisher = event_publisher

    def confirm_payment(self, command: ConfirmPaymentCommand) -> ConfirmPaymentResult:
        transaction = self.transaction_repository.get_by_id(command.transaction_id)
        if transaction is None:
            raise ValueError("transaction not found")

        confirmed_at = transaction.confirm()
        self.transaction_repository.save(transaction)
        self.event_publisher.publish_payment_confirmed(
            PaymentConfirmed(
                transaction_id=transaction.id,
                customer_id=command.customer_id,
                merchant_id=transaction.merchant_id or "",
                account_id=command.account_id,
                amount=command.amount,
                confirmed_at=confirmed_at,
            )
        )
        return ConfirmPaymentResult(
            transaction_id=transaction.id,
            status=transaction.status,
            confirmed_at=confirmed_at,
        )
