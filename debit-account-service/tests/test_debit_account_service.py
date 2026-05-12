from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from application.schemas import DebitAccountCommand
from application.services.debit_account_service import DebitAccountService
from domain.account import Account
from domain.debit_status import DebitStatus


class InMemoryAccountRepository:
    def __init__(self):
        self.accounts = {}

    def save(self, account):
        self.accounts[account.customer_id] = account

    def get_by_customer_id(self, customer_id):
        return self.accounts.get(customer_id)


def test_debit_account_completes_and_publishes_event():
    repository = InMemoryAccountRepository()
    account = Account.create("customer-1", "Customer One", Decimal("100.00"))
    repository.save(account)
    publisher = InMemoryEventPublisher()
    service = DebitAccountService(repository, publisher)

    result = service.debit_account(
        DebitAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )

    assert result.status == DebitStatus.COMPLETED
    assert result.account_id == account.id
    assert account.balance == Decimal("70.00")
    assert len(account.entries) == 1
    assert len(publisher.completed_events) == 1
    assert publisher.failed_events == []

    event = publisher.completed_events[0]
    assert event.event_name == "DebitCompleted"
    assert event.transaction_id == "transaction-1"
    assert event.account_id == account.id
    assert event.merchant_id == "merchant-1"


def test_debit_account_fails_when_account_not_found():
    repository = InMemoryAccountRepository()
    publisher = InMemoryEventPublisher()
    service = DebitAccountService(repository, publisher)

    result = service.debit_account(
        DebitAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )

    assert result.status == DebitStatus.FAILED
    assert result.account_id is None
    assert result.reason == "ACCOUNT_NOT_FOUND"
    assert publisher.completed_events == []
    assert len(publisher.failed_events) == 1
    assert publisher.failed_events[0].reason == "ACCOUNT_NOT_FOUND"


def test_debit_account_fails_when_balance_is_insufficient():
    repository = InMemoryAccountRepository()
    account = Account.create("customer-1", "Customer One", Decimal("10.00"))
    repository.save(account)
    publisher = InMemoryEventPublisher()
    service = DebitAccountService(repository, publisher)

    result = service.debit_account(
        DebitAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )

    assert result.status == DebitStatus.FAILED
    assert result.account_id == account.id
    assert result.reason == "INSUFFICIENT_BALANCE"
    assert account.balance == Decimal("10.00")
    assert publisher.completed_events == []
    assert len(publisher.failed_events) == 1
