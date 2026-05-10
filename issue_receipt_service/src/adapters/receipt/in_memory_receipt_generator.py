import json

from domain.receipt import Receipt


class InMemoryReceiptGenerator:
    def generate(self, receipt: Receipt) -> str:
        return json.dumps(
            {
                "receipt_type": "PAYMENT_CONFIRMATION",
                "transaction_id": receipt.transaction_id,
                "customer_id": receipt.customer_id,
                "merchant_id": receipt.merchant_id,
                "amount": str(receipt.amount),
                "confirmed_at": receipt.confirmed_at.isoformat(),
            }
        )
