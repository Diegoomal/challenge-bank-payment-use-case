from typing import Protocol

from application.schemas import IssueReceiptCommand, IssueReceiptResult


class ForIssuingReceipt(Protocol):
    def issue_receipt(self, command: IssueReceiptCommand) -> IssueReceiptResult:
        pass
