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


# Making orders
order = Order()
order.add_item("Clean Architecture Book, Uncle Bob", 1, 100)
order.add_item("Speaker", 1, 30)
order.add_item("HDMI Cable", 3, 10)
order.add_item("PIR Sensor", 2, 7)

print(order.total_price())


# Payment using Debit card
order.pay("debit", "123456789")
