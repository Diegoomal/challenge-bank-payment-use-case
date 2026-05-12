from enum import Enum


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    WEBHOOK = "WEBHOOK"
