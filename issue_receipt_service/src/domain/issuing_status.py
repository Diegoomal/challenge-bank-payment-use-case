from enum import Enum


class IssuingStatus(str, Enum):
    PENDING = "PENDING"
    ISSUED = "ISSUED"
    FAILED = "FAILED"
