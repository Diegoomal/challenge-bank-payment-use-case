from application.services.issue_receipt_service import IssueReceiptService


class StartPaymentService(IssueReceiptService):
    def start_payment(self, command):
        return self.issue_receipt(command)
