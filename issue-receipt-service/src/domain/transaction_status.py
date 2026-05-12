from enum import Enum


class TransactionStatus(str, Enum):
    STARTED = "STARTED"
    PROCESSING = "PROCESSING"
    CONFIRMED = "CONFIRMED"
    REVERSED = "REVERSED"
    FAILED = "FAILED"
