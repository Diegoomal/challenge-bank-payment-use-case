from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CustomerNotified:
    notification_id: str
    transaction_id: str
    customer_id: str
    notification_type: str
    amount: Decimal
    channel: str
    status: str
    notified_at: datetime

    @property
    def event_name(self) -> str:
        return "CustomerNotified"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "notification_id": self.notification_id,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "notification_type": self.notification_type,
            "amount": str(self.amount),
            "channel": self.channel,
            "status": self.status,
            "notified_at": self.notified_at.isoformat(),
        }


MerchantNotified = CustomerNotified
