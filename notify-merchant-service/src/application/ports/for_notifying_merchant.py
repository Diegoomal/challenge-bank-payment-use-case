from typing import Protocol

from application.schemas import NotifyMerchantCommand, NotifyMerchantResult


class ForNotifyingMerchant(Protocol):
    def notify_merchant(
        self,
        command: NotifyMerchantCommand,
    ) -> NotifyMerchantResult:
        pass
