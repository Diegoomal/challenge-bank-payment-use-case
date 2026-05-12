from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class MerchantNotified:
    notification_id: str
    transaction_id: str
    merchant_id: str
    amount: Decimal
    channel: str
    status: str
    notified_at: datetime

    @property
    def event_name(self) -> str:
        return "MerchantNotified"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "notification_id": self.notification_id,
            "transaction_id": self.transaction_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "channel": self.channel,
            "status": self.status,
            "notified_at": self.notified_at.isoformat(),
        }
