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


class SMSAuthorizer:

    authorized = False

    def verify_code(self, code):
        print(f"Verifying code {code}")
        self.authorized = True

    def is_authorized(self):
        return self.authorized


class PaymentHandler(ABC):
    @abstractmethod
    def pay(self, order: Order):
        pass


class DebitPaymentHandler(PaymentHandler):
    def __init__(self, security_code, authorizer: SMSAuthorizer):
        self.authorizer = authorizer
        self.security_code = security_code

    def pay(self, order: Order):
        if not self.authorizer.is_authorized():
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


class PayPalPaymentHandler(PaymentHandler):
    def __init__(self, email, authorizer: SMSAuthorizer) -> None:
        self.authorizer = authorizer
        self.email = email

    def pay(self, order: Order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authenticated")
        print("Processing PayPal payment...")
        print(f"Verifying email: {self.email}.")
        order.status = "paid"


# Making orders
order = Order()
order.add_item("Head First Object Oriented Analysis and Design Book", 1, 76)
order.add_item("Raspberry Pi Camera v2", 2, 40)

print(order.total_price())


# SMS Authorizer
sms_authorizer = SMSAuthorizer()

# Payment using Debit Card

debit_payment = DebitPaymentHandler("67891", sms_authorizer)
sms_authorizer.verify_code("24682")
debit_payment.pay(order)
