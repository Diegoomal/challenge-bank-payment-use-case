from application.services.notify_customer_service import NotifyCustomerService


class NotifyMerchantService(NotifyCustomerService):
    def notify_merchant(self, command):
        return self.notify_customer(command)
