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

After a while, Mohammad bought some books and read some articles talking about SOLID principles! And he decided to SOLID-ify his program.

**SOLID** stands for:
- **S**: Single responsibility principle.
- **O**: Open–closed principle.
- **L**: Liskov substitution principle.
- **I**: Interface segregation principle.
- **D**: Dependency inversion principle.

-------

### Single Responsibility Principle (SRP)

The SRP dictates that **classes should have only a single reason to change**. If your calss have multiple reasons for change; then it indicates that your class is tightly-coupled and harder to maintain.

<p align="center">
<img src="assets/srp.jpg" width=30% height=25%>
</p>

At this moment, Mohammad asks himself; "What are the responsibilities of `Order` class at my code?" He finds that the class have different responsibilities such as: adding items, calculating total price and payment details.

Some of these responsibilities are fine to be there, but others aren't.

Then he said: "What if I decided to accept a new payment method like Bitcoin? ApplePay?". Then,He decided to split the payment responsibility out of `Order` class.

The change after applying SRP is:

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

Output will be:
```python
174
Processing Credit Card payment...
Verifying code: 543219876.
```

Changes in the example above are for demonstration purposes, Mohammad can do more work to optimize this code such as creating a special method for changing the status of order and more.

[For more details about SRP, take a look on Uncle Bob's blog from [here](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)]