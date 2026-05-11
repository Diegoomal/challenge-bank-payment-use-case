from enum import Enum


class NotificationType(str, Enum):
    PAYMENT_CONFIRMED = "PAYMENT_CONFIRMED"
    PAYMENT_REVERSED = "PAYMENT_REVERSED"
