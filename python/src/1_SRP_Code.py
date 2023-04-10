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
