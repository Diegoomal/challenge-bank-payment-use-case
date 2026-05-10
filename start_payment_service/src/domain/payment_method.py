from enum import Enum


class PaymentMethod(str, Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    ACCOUNT_BALANCE = "ACCOUNT_BALANCE"
    PIX = "PIX"
