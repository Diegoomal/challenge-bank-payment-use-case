from application.ports.event_publisher import EventPublisher
from application.ports.for_reversing_payment import ForReversingPayment
from application.ports.transaction_repository import TransactionRepository
from application.schemas import ReversePaymentCommand, ReversePaymentResult
from domain.events import PaymentReversed
from domain.transaction_status import TransactionStatus


class ReversePaymentService(ForReversingPayment):
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.event_publisher = event_publisher

    def reverse_payment(self, command: ReversePaymentCommand) -> ReversePaymentResult:
        transaction = self.transaction_repository.get_by_id(command.transaction_id)
        if transaction is None:
            raise ValueError("transaction not found")

        if transaction.status == TransactionStatus.REVERSED:
            return ReversePaymentResult(
                transaction_id=transaction.id,
                status=transaction.status,
                reversed_at=transaction.reversed_at,
                reason=transaction.reversal_reason,
            )

        reversed_at = transaction.reverse(command.reason)
        self.transaction_repository.save(transaction)
        self.event_publisher.publish_payment_reversed(
            PaymentReversed(
                transaction_id=transaction.id,
                customer_id=command.customer_id,
                merchant_id=command.merchant_id or transaction.merchant_id or "",
                amount=command.amount,
                reason=command.reason,
                reversed_at=reversed_at,
            )
        )
        return ReversePaymentResult(
            transaction_id=transaction.id,
            status=transaction.status,
            reversed_at=reversed_at,
            reason=command.reason,
        )
