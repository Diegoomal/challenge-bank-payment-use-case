from decimal import Decimal

import pytest

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from application.schemas import CreateAccountCommand
from application.services.create_account_service import CreateAccountService
from domain.account_status import AccountStatus


class InMemoryAccountRepository:
    def __init__(self):
        self.accounts = {}

    def save(self, account):
        self.accounts[account.customer_id] = account

    def get_by_customer_id(self, customer_id):
        return self.accounts.get(customer_id)

    def has_active_account(self, customer_id):
        account = self.accounts.get(customer_id)
        return account is not None and account.status == AccountStatus.ACTIVE


def test_create_account_persists_account_and_publishes_event():
    repository = InMemoryAccountRepository()
    publisher = InMemoryEventPublisher()
    service = CreateAccountService(repository, publisher)

    result = service.create_account(
        CreateAccountCommand("customer-1", "Customer One", Decimal("100.00"))
    )

    account = repository.get_by_customer_id("customer-1")
    assert result.account_id == account.id
    assert result.status == AccountStatus.ACTIVE
    assert len(publisher.created_events) == 1
    assert publisher.created_events[0].event_name == "AccountCreated"
    assert publisher.created_events[0].account_id == account.id


def test_create_account_rejects_customer_with_active_account():
    repository = InMemoryAccountRepository()
    publisher = InMemoryEventPublisher()
    service = CreateAccountService(repository, publisher)
    service.create_account(
        CreateAccountCommand("customer-1", "Customer One", Decimal("100.00"))
    )

    with pytest.raises(ValueError, match="customer already has an active account"):
        service.create_account(
            CreateAccountCommand("customer-1", "Customer One", Decimal("50.00"))
        )

    assert len(publisher.created_events) == 1
