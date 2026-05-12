from enum import Enum


class DebitStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
