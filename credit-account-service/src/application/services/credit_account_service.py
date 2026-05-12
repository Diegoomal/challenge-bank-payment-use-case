from datetime import datetime, timezone

from application.ports.account_repository import AccountRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_crediting_account import ForCreditingAccount
from application.schemas import CreditAccountCommand, CreditAccountResult
from domain.credit_status import CreditStatus
from domain.events import CreditCompleted, CreditFailed


class CreditAccountService(ForCreditingAccount):
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.account_repository = account_repository
        self.event_publisher = event_publisher

    def credit_account(self, command: CreditAccountCommand) -> CreditAccountResult:
        account = self.account_repository.get_by_customer_id(command.merchant_id)
        if account is None:
            self._publish_failed(command, "MERCHANT_ACCOUNT_NOT_FOUND")
            return CreditAccountResult(
                account_id=None,
                transaction_id=command.transaction_id,
                status=CreditStatus.FAILED,
                reason="MERCHANT_ACCOUNT_NOT_FOUND",
            )

        try:
            account.credit(command.transaction_id, command.amount)
        except ValueError as error:
            self._publish_failed(command, str(error))
            return CreditAccountResult(
                account_id=account.id,
                transaction_id=command.transaction_id,
                status=CreditStatus.FAILED,
                reason=str(error),
            )

        self.account_repository.save(account)
        self.event_publisher.publish_credit_completed(
            CreditCompleted(
                transaction_id=command.transaction_id,
                account_id=account.id,
                customer_id=command.customer_id,
                merchant_id=account.customer_id,
                amount=command.amount,
                credited_at=datetime.now(timezone.utc),
            )
        )
        return CreditAccountResult(
            account_id=account.id,
            transaction_id=command.transaction_id,
            status=CreditStatus.COMPLETED,
        )

    def _publish_failed(self, command: CreditAccountCommand, reason: str) -> None:
        self.event_publisher.publish_credit_failed(
            CreditFailed(
                transaction_id=command.transaction_id,
                customer_id=command.customer_id,
                merchant_id=command.merchant_id,
                amount=command.amount,
                reason=reason,
                failed_at=datetime.now(timezone.utc),
            )
        )
