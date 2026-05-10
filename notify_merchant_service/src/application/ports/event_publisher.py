from typing import Protocol

from domain.events import MerchantNotified


class EventPublisher(Protocol):
    def publish_merchant_notified(self, event: MerchantNotified) -> None:
        pass
