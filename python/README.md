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

After a while, Mohammad bought a book titled: `Clean Architecture` by Robert C. Martin.

In this book, he read about SOLID principles, and he decided to SOLID-ify his program.

### Single Responsibility Principle (SRP)

