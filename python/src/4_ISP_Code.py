from abc import ABC, abstractmethod


class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


class PaymentHandler(ABC):
    @abstractmethod
    def pay(self, order: Order):
        pass


class SMSPaymentAuthHandler(PaymentHandler):
    @abstractmethod
    def auth_2fa_sms(self, code):
        pass


class DebitPaymentHandler(SMSPaymentAuthHandler):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False

    def auth_2fa_sms(self, code):
        print(f"Verifying 2FA using SMS code: {code}")
        self.verified = True

    def pay(self, order: Order):
        if not self.verified:
            raise Exception("Not authenticated")
        print("Processing Debit Card payment...")
        print(f"Verifying code: {self.security_code}.")
        order.status = "paid"


class CreditPaymentHandler(PaymentHandler):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order: Order):
        print("Processing Credit Card payment...")
        print(f"Verifying code: {self.security_code}.")
        order.status = "paid"


class PayPalPaymentHandler(SMSPaymentAuthHandler):
    def __init__(self, email) -> None:
        self.email = email

    def auth_2fa_sms(self, code):
        print(f"Verifying 2FA using SMS code: {code}")
        self.verified = True

    def pay(self, order: Order):
        if not self.verified:
            raise Exception("Not authenticated")
        print("Processing PayPal payment...")
        print(f"Verifying email: {self.email}.")
        order.status = "paid"


# Making orders
order = Order()
order.add_item("Head First Object Oriented Analysis and Design Book", 1, 76)
order.add_item("Raspberry Pi Camera v2", 2, 40)

print(order.total_price())


# Payment using Debit Card

debit_payment = DebitPaymentHandler("67891")
debit_payment.auth_2fa_sms("54321")
debit_payment.pay(order)

print("#"*20)

# Payment using Credit Card

credit_payment = CreditPaymentHandler("97531")
credit_payment.pay(order)
