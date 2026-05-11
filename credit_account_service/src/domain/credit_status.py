from enum import Enum


class CreditStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
