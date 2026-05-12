from datetime import datetime, timezone

from application.ports.account_repository import AccountRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_creating_account import ForCreatingAccount
from application.schemas import CreateAccountCommand, CreateAccountResult
from domain.account import Account
from domain.events import AccountCreated


class CreateAccountService(ForCreatingAccount):
    def __init__(
        self,
        account_repository: AccountRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.account_repository = account_repository
        self.event_publisher = event_publisher

    def create_account(self, command: CreateAccountCommand) -> CreateAccountResult:
        if self.account_repository.has_active_account(command.customer_id):
            raise ValueError("customer already has an active account")

        account = Account.create(
            customer_id=command.customer_id,
            account_holder=command.account_holder,
            initial_deposit=command.initial_deposit,
        )
        self.account_repository.save(account)
        self.event_publisher.publish_account_created(
            AccountCreated(
                account_id=account.id,
                customer_id=account.customer_id,
                account_holder=account.account_holder,
                initial_deposit=account.balance,
                occurred_at=datetime.now(timezone.utc),
            )
        )
        return CreateAccountResult(
            account_id=account.id,
            customer_id=account.customer_id,
            status=account.status,
            created_at=account.created_at,
        )
