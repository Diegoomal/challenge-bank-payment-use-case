from application.ports.event_publisher import EventPublisher
from application.ports.for_issuing_receipt import ForIssuingReceipt
from application.ports.receipt_generator import ReceiptGenerator
from application.ports.receipt_repository import ReceiptRepository
from application.schemas import IssueReceiptCommand, IssueReceiptResult
from domain.events import ReceiptIssued
from domain.issuing_status import IssuingStatus
from domain.receipt import Receipt


class IssueReceiptService(ForIssuingReceipt):
    def __init__(
        self,
        receipt_repository: ReceiptRepository,
        receipt_generator: ReceiptGenerator,
        event_publisher: EventPublisher,
    ) -> None:
        self.receipt_repository = receipt_repository
        self.receipt_generator = receipt_generator
        self.event_publisher = event_publisher

    def issue_receipt(self, command: IssueReceiptCommand) -> IssueReceiptResult:
        receipt = self.receipt_repository.get_by_transaction_id(command.transaction_id)
        if receipt is not None and receipt.status == IssuingStatus.ISSUED:
            return self._to_result(receipt)

        if receipt is None:
            receipt = Receipt.create_pending(
                transaction_id=command.transaction_id,
                customer_id=command.customer_id,
                merchant_id=command.merchant_id,
                amount=command.amount,
                confirmed_at=command.confirmed_at,
            )

        try:
            document_data = self.receipt_generator.generate(receipt)
            issued_at = receipt.issue(document_data)
        except Exception as error:
            receipt.fail(str(error))
            self.receipt_repository.save(receipt)
            return self._to_result(receipt)

        self.receipt_repository.save(receipt)
        self.event_publisher.publish_receipt_issued(
            ReceiptIssued(
                receipt_id=receipt.id,
                transaction_id=receipt.transaction_id,
                customer_id=receipt.customer_id,
                merchant_id=receipt.merchant_id,
                amount=receipt.amount,
                issued_at=issued_at,
            )
        )
        return self._to_result(receipt)

    @staticmethod
    def _to_result(receipt: Receipt) -> IssueReceiptResult:
        return IssueReceiptResult(
            receipt_id=receipt.id,
            transaction_id=receipt.transaction_id,
            status=receipt.status,
            issued_at=receipt.issued_at,
        )
