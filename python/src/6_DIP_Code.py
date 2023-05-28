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


class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self):
        pass


class reCAPTCHA_Authorizer(Authorizer):

    authorized = False

    def verify_reCAPTCHA(self, user_selections):
        print(f"Verifying reCAPTCHA {user_selections}")
        print("User passed `I'm not a robot' test")
        self.authorized = True

    def is_authorized(self):
        return self.authorized


class SMSAuthorizer(Authorizer):

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
    def __init__(self, security_code, authorizer: Authorizer):
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
    def __init__(self, email, authorizer: Authorizer) -> None:
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
order.add_item("Domain Driven Design Book, by Eric Evans", 2, 111)
order.add_item("Raspberry Pi Pico", 3, 15)

print(order.total_price())


# reCAPTCHA Authorizer
reCAPTCHA_authorizer = reCAPTCHA_Authorizer()

# Payment using PayPal

paypal_payment = PayPalPaymentHandler("hi@customer.com", reCAPTCHA_authorizer)
reCAPTCHA_authorizer.verify_reCAPTCHA("User Selections: 1,4,7")
paypal_payment.pay(order)
