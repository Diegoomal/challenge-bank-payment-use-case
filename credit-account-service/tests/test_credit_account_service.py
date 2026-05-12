from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from application.schemas import CreditAccountCommand
from application.services.credit_account_service import CreditAccountService
from domain.account import Account
from domain.credit_status import CreditStatus


class InMemoryAccountRepository:
    def __init__(self):
        self.accounts = {}

    def save(self, account):
        self.accounts[account.customer_id] = account

    def get_by_customer_id(self, customer_id):
        return self.accounts.get(customer_id)


def test_credit_account_completes_and_publishes_event():
    repository = InMemoryAccountRepository()
    account = Account.create("merchant-1", "Merchant One", Decimal("100.00"))
    repository.save(account)
    publisher = InMemoryEventPublisher()
    service = CreditAccountService(repository, publisher)

    result = service.credit_account(
        CreditAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )

    assert result.status == CreditStatus.COMPLETED
    assert result.account_id == account.id
    assert account.balance == Decimal("130.00")
    assert len(account.entries) == 1
    assert len(publisher.completed_events) == 1
    assert publisher.failed_events == []

    event = publisher.completed_events[0]
    assert event.event_name == "CreditCompleted"
    assert event.transaction_id == "transaction-1"
    assert event.account_id == account.id
    assert event.customer_id == "customer-1"
    assert event.merchant_id == "merchant-1"


def test_credit_account_fails_when_account_not_found():
    repository = InMemoryAccountRepository()
    publisher = InMemoryEventPublisher()
    service = CreditAccountService(repository, publisher)

    result = service.credit_account(
        CreditAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )

    assert result.status == CreditStatus.FAILED
    assert result.account_id is None
    assert result.reason == "MERCHANT_ACCOUNT_NOT_FOUND"
    assert publisher.completed_events == []
    assert len(publisher.failed_events) == 1
    assert publisher.failed_events[0].reason == "MERCHANT_ACCOUNT_NOT_FOUND"


def test_credit_account_is_idempotent_by_transaction_id():
    repository = InMemoryAccountRepository()
    account = Account.create("merchant-1", "Merchant One", Decimal("10.00"))
    repository.save(account)
    publisher = InMemoryEventPublisher()
    service = CreditAccountService(repository, publisher)

    first = service.credit_account(
        CreditAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )
    second = service.credit_account(
        CreditAccountCommand(
            "transaction-1",
            "customer-1",
            "merchant-1",
            Decimal("30.00"),
        )
    )

    assert first.status == CreditStatus.COMPLETED
    assert second.status == CreditStatus.COMPLETED
    assert account.balance == Decimal("40.00")
    assert len(account.entries) == 1
