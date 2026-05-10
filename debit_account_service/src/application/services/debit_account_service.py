from datetime import datetime, timezone

from application.ports.account_repository import AccountRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_debiting_account import ForDebitingAccount
from application.schemas import DebitAccountCommand, DebitAccountResult
from domain.debit_status import DebitStatus
from domain.events import DebitCompleted, DebitFailed
from domain.exceptions import InsufficientBalance


class DebitAccountService(ForDebitingAccount):
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.account_repository = account_repository
        self.event_publisher = event_publisher

    def debit_account(self, command: DebitAccountCommand) -> DebitAccountResult:
        account = self.account_repository.get_by_customer_id(command.customer_id)
        if account is None:
            self._publish_failed(command, "ACCOUNT_NOT_FOUND")
            return DebitAccountResult(
                account_id=None,
                transaction_id=command.transaction_id,
                status=DebitStatus.FAILED,
                reason="ACCOUNT_NOT_FOUND",
            )

        try:
            account.debit(command.transaction_id, command.amount)
        except InsufficientBalance:
            self._publish_failed(command, "INSUFFICIENT_BALANCE")
            return DebitAccountResult(
                account_id=account.id,
                transaction_id=command.transaction_id,
                status=DebitStatus.FAILED,
                reason="INSUFFICIENT_BALANCE",
            )
        except ValueError as error:
            self._publish_failed(command, str(error))
            return DebitAccountResult(
                account_id=account.id,
                transaction_id=command.transaction_id,
                status=DebitStatus.FAILED,
                reason=str(error),
            )

        self.account_repository.save(account)
        self.event_publisher.publish_debit_completed(
            DebitCompleted(
                transaction_id=command.transaction_id,
                account_id=account.id,
                customer_id=account.customer_id,
                amount=command.amount,
                occurred_at=datetime.now(timezone.utc),
            )
        )
        return DebitAccountResult(
            account_id=account.id,
            transaction_id=command.transaction_id,
            status=DebitStatus.COMPLETED,
        )

    def _publish_failed(self, command: DebitAccountCommand, reason: str) -> None:
        self.event_publisher.publish_debit_failed(
            DebitFailed(
                transaction_id=command.transaction_id,
                customer_id=command.customer_id,
                amount=command.amount,
                reason=reason,
                occurred_at=datetime.now(timezone.utc),
            )
        )
