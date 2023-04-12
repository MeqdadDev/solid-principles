# SOLID Principles with Python

Let's build a story! To see how to bring SOLID principles to life.

### The Beginning

Meet Mohammad, a smart person who wants to build a robust payment system.

First of all, Mohammad thinks to create a class with different responsibilities from adding items, calculating prices to create verification process and payment using various types.

Code Example:
```python
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

    def pay(self, payment_type, security_code):
        if payment_type == "debit":
            print("Processing payment type...")
            print(f"Verifying code: {security_code}.")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing payment type...")
            print(f"Verifying code: {security_code}.")
            self.status = "paid"
        else:
            raise Exception(f"#### Unknown type: {payment_type}.")

```

To use this class in code, Mohammad created this use case:

```python
# Making orders
order = Order()
order.add_item("Clean Architecture Book, Uncle Bob", 1, 100)
order.add_item("Speaker", 1, 30)
order.add_item("HDMI Cable", 3, 10)
order.add_item("PIR Sensor", 2, 7)

print(order.total_price())

# Payment using Debit card
order.pay("debit", "123456789")
```

The output was:

```python
174
Processing payment type...
Verifying code: 123456789.
```

Everything works fine and it's OK for now.

-------

### SOLID Principles

For the purpose of our story, we will presume the presence of a consultant known as "**Uncle Clean**" who is tasked with providing Mohammad with advice and insights for the implementation of SOLID principles in his program.

**SOLID** stands for:
- **S**: Single responsibility principle.
- **O**: Open–closed principle.
- **L**: Liskov substitution principle.
- **I**: Interface segregation principle.
- **D**: Dependency inversion principle.

-------

### Single Responsibility Principle (SRP)

At this moment, Mohammad asks himself; "What are the responsibilities of `Order` class at my code?" He finds that the class have different responsibilities such as: adding items, calculating total price and payment details.

#### Uncle Clean in the Scene

Uncle Clean: Hi Mohammad, did you hear about SRP?

Mohammad: No, what is SRP?

Uncle Clean:

The SRP dictates that **classes should have only a single reason to change**. If your class contains multiple reasons for change; then it indicates that your code is tightly-coupled and harder to maintain.

<p align="center">
<img src="assets/srp.jpg" width=40% height=30%>
</p>

Uncle Clean:

What if a new customer came to you and asked for a new payment method like Bitcoin? PayPal? Then you need to change the `Order` class!. I suggest on you to split the payment responsibility out of `Order` class.

After this advice, Mohammad changed his code to the following one:

```python
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


class PaymentHandler:
    def pay_debit(self, order: Order, security_code):
        print("Processing Debit Card payment...")
        print(f"Verifying code: {security_code}.")
        order.status = "paid"

    def pay_credit(self, order: Order, security_code):
        print("Processing Credit Card payment...")
        print(f"Verifying code: {security_code}.")
        order.status = "paid"


# Making orders
order = Order()
order.add_item("Clean Architecture Book, Uncle Bob", 1, 100)
order.add_item("Speaker", 1, 30)
order.add_item("HDMI Cable", 3, 10)
order.add_item("PIR Sensor", 2, 7)

print(order.total_price())


# Payment using Credit card
payment_handler = PaymentHandler()
payment_handler.pay_credit(order, "543219876")
```

Output:

```python
174
Processing Credit Card payment...
Verifying code: 543219876.
```

Uncle Clean:

Good job Mohammad, you're doing great, also you can do more work to optimize this code such as creating a special method for changing the status of order and more. But this is fine for now.

[For more details about SRP, take a look on Uncle Bob's blog from [here](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)]

-------

### Open/Closed Principle (OCP)


After some days, a new client approached Mohammad and inquired about the availability of PayPal payment support in his program. Mohammad responded by stating that this functionality could be easily incorporated.

To achieve that, Mohammad created a new method for PayPal, but he made a mistake while calling it, he used `pay_debit` instead of using `pay_PayPal`. Mohammad encountered additional comparable issues, which led him to realize that he was frequently modifying the `PaymentHandler` class each time a new payment feature was introduced.

#### Uncle Clean in the Scene

Uncle Clean: Hi Mohammad, After reviewing your recent difficulties when attempting to integrate new payment methods, my recommendation is to take the OCP into account as you continue to develop your code.

Mohammad: What is OCP?

Uncle Clean:

OCP stands for **Open/Closed Principle (OCP)** which states that software entities (classes, functions, ...) should be **open for extension** but **closed for modification**. This means that when new requirements arise or changes need to be made, it should be possible to extend the behavior of the software entity without modifying its source code.

<p align="center">
<img src="assets/ocp.jpg" width=40% height=30%>
</p>

Now, after considering OCP into account, the new code became:

```python
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
    def pay(self, order: Order, security_code):
        pass


class DebitPaymentHandler(PaymentHandler):
    def pay(self, order: Order, security_code):
        print("Processing Debit Card payment...")
        print(f"Verifying code: {security_code}.")
        order.status = "paid"


class CreditPaymentHandler(PaymentHandler):
    def pay(self, order: Order, security_code):
        print("Processing Credit Card payment...")
        print(f"Verifying code: {security_code}.")
        order.status = "paid"


class PayPalPaymentHandler(PaymentHandler):
    def pay(self, order: Order, security_code):
        print("Processing PayPal payment...")
        print(f"Verifying code: {security_code}.")
        order.status = "paid"


# Making orders
order = Order()
order.add_item("The Pragmatic Programmer Book, Andy Hunt", 1, 130)
order.add_item("micro:bit Controller", 5, 14)

print(order.total_price())


# Payment using PayPal

paypal_payment = PayPalPaymentHandler()
paypal_payment.pay(order, "543219876")
```

Output:
```
200
Processing PayPal payment...
Verifying code: 543219876.
```
