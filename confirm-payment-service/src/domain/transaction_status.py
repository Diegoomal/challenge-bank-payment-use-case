from enum import Enum


class TransactionStatus(str, Enum):
    STARTED = "STARTED"
    CONFIRMED = "CONFIRMED"
    REVERSED = "REVERSED"
    FAILED = "FAILED"
