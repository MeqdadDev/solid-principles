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


class DebitPaymentHandler(PaymentHandler):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order: Order):
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
    def __init__(self, email) -> None:
        self.email = email

    def pay(self, order: Order):
        print("Processing PayPal payment...")
        print(f"Verifying email: {self.email}.")
        order.status = "paid"


# Making orders
order = Order()
order.add_item("The Pragmatic Programmer Book, Andy Hunt", 1, 130)
order.add_item("micro:bit Controller", 5, 14)

print(order.total_price())


# Payment using PayPal

paypal_payment = PayPalPaymentHandler("hi@cutomer.com")
paypal_payment.pay(order)
