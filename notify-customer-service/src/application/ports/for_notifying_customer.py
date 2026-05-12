from typing import Protocol

from application.schemas import NotifyCustomerCommand, NotifyCustomerResult


class ForNotifyingCustomer(Protocol):
    def notify_customer(
        self,
        command: NotifyCustomerCommand,
    ) -> NotifyCustomerResult:
        pass
