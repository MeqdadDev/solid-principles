# SOLID Principles with Python

<p align="center">
<img src="assets/solid.jpg" width=40% height=30%>
</p>

Let's build a story! To see how to bring SOLID principles to life.

### The Beginning

Meet Mohammad, a smart person who wants to build a robust payment system.

First of all, Mohammad thinks to create a class with different responsibilities from adding items, calculating prices to create verification process and payment using various types.

System initial code:
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

Output:
```bash
174
Processing payment type...
Verifying code: 123456789.
```

Everything works fine and it's OK for now.

-------

### SOLID Principles

Let's assume that "**Uncle Clean**", a consultant, is helping Mohammad implement the SOLID principles in his program.

**SOLID** stands for:
- **S**: Single responsibility principle.
- **O**: Open–closed principle.
- **L**: Liskov substitution principle.
- **I**: Interface segregation principle.
- **D**: Dependency inversion principle.

-------

### 1- Single Responsibility Principle (SRP)

<p align="center">
<img src="assets/srp.jpg" width=40% height=30%>
</p>

At this moment, Mohammad asks himself; "What are the responsibilities of `Order` class at my code?" He finds that the class have different responsibilities such as: adding items, calculating total price and payment details.

#### Uncle Clean in the Scene

Uncle Clean: Hi Mohammad, did you hear about SRP?

Mohammad: No, what is SRP?

Uncle Clean:

The SRP dictates that **classes should have only a single reason to change**. If your class contains multiple reasons for change; then it indicates that your code is tightly-coupled and harder to maintain.


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

```bash
174
Processing Credit Card payment...
Verifying code: 543219876.
```

Uncle Clean:

Good job Mohammad, you're doing great, also you can do more work to optimize this code such as creating a special method for changing the status of order and more. But this is fine for now.

[For more details about SRP, take a look on Uncle Bob's blog from [here](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)]

-------

### 2- Open/Closed Principle (OCP)

<p align="center">
<img src="assets/ocp.jpg" width=40% height=30%>
</p>

After some days, a new client approached Mohammad and inquired about the availability of PayPal payment support in his program. Mohammad responded by stating that this functionality could be easily incorporated.

To achieve that, Mohammad created a new method for PayPal, but he made a mistake while calling it, he used `pay_debit` instead of using `pay_PayPal`. Mohammad encountered additional comparable issues, which led him to realize that he was frequently modifying the `PaymentHandler` class each time a new payment feature was introduced.

#### Uncle Clean in the Scene

Uncle Clean: Hi Mohammad, After reviewing your recent difficulties when attempting to integrate new payment methods, my recommendation is to take the OCP into account as you continue to develop your code.

Mohammad: What is OCP?

Uncle Clean:

OCP stands for **Open/Closed Principle (OCP)** which states that software entities (classes, functions, ...) should be **open for extension** but **closed for modification**. This means that when new requirements arise or changes need to be made, it should be possible to extend the behavior of the software entity without modifying its source code.

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
```bash
200
Processing PayPal payment...
Verifying code: 543219876.
```

-------

### 3- Liskov Substitution Principle (LSP)

<p align="center">
<img src="assets/lsp.jpg" width=40% height=30%>
</p>

Next day after adding PayPal payment integration, a customer called Mohammad and told him that there is a big issue in the system! Paying using PayPal method doesn't require security code! it requires email!

Mohammad start thinking about changing the `security_code` to `email`, BUT... Changing this to `email` will create a new problem with other payment methods which require `security_code`.

#### Uncle Clean in the Scene

Uncle Clean: Hey Mohammad, I heard about your last problem, why you won't use Liskov?

Mohammad: Hey Uncle, what you're talking about? Liskov???

Uncle Clean:

LSP is created by Prof. Barbara Liskov which stands for **Liskov Substitution Principle**, which states that objects of a superclass should be replaceable with objects of its subclasses without breaking the program's behavior.


The result of applying Liskov Substitution Principle on the codebase was:

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

paypal_payment = PayPalPaymentHandler("hi@customer.com")
paypal_payment.pay(order)
```

Output:

```bash
200
Processing PayPal payment...
Verifying email: hi@customer.com.
```


-------

### 4- Interface Segregation Principle (ISP)

<p align="center">
<img src="assets/isp.jpg" width=40% height=30%>
</p>

After a while, Mohammad contacted a cyber security expert to review the whole system and to submit a report that helps him to fix the vulnerabilities in the system for more protection.

One of the main points that this cyber security expert mentioned in his report: Adding 2FA ( Two-factor Authentication) to the system.

Based on that, Mohammad started to work on this feature by adding authentication method using SMS `auth_2fa_sms` in the `PaymentHandler`. And he implemented it to the other classes that are inheriting from the base class.

The code became as the following:

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
    def auth_2fa_sms(self, code):
        pass

    @abstractmethod
    def pay(self, order: Order):
        pass


class DebitPaymentHandler(PaymentHandler):
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

    def auth_2fa_sms(self, code):
        # It is also a violation for Liskov Substitution principle
        raise Exception(
            "Credit card payment doesn't support SMS code authentication.")

    def pay(self, order: Order):
        print("Processing Credit Card payment...")
        print(f"Verifying code: {self.security_code}.")
        order.status = "paid"


class PayPalPaymentHandler(PaymentHandler):
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
```

As in the above code, when the user pay for his stuff using debit card, it should be authenticated before payment process, and the expected result will be as the following:

```bash
156
Verifying 2FA using SMS code: 54321
Processing Debit Card payment...
Verifying code: 67891.
```

#### Uncle Clean in the Scene

Uncle Clean: Hello Abo Ehmaid (a nickname for Mohammad), I heard that you're securing your payment software, a good news!
But what will happen if the user start using credit card?

Mohammad: Hi uncle, I know that credit card doesn't support 2FA using SMS verification, so I added an exception for this error. But I think it should be implemented in a better way. What do you advise me to do?

Uncle Clean: I suggest on you to use interface segregation.

Mohammad: ?????

Uncle Clean: **Interface Segregation Principle (ISP)** means: Clients should not be forced to depend on interfaces they do not use (SMS 2FA with credit card in your case).

Mohammad: I'll read about it and fix that.

After reading using different resources about ISP, Mohammad ended up with this modification:

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
```

Output:
```bash
156
Verifying 2FA using SMS code: 54321
Processing Debit Card payment...
Verifying code: 67891.
####################
Processing Credit Card payment...
Verifying code: 97531.
```

-------

### Composition over Inheritance

<p align="center">
<img src="assets/coi.jpg" width=40% height=30%>
</p>

***Note: Composition over Inheritance is not one of the SOLID principles, but it is worth mentioning in the story context because it is more efficient in this case.***

#### Uncle Clean in the Scene

Uncle Clean: Hi Mohammad, you did a good job by separating the interfaces.

Mohammad: Thanks uncle, your follow up and advices for me are highly appreciated.

Uncle Clean: Are you familiar with various types of two-factor authentication (2FA) methods?

Mohammad: Yes, I am. I know different types, such as SMS-based, authenticator apps, Email-based, and more.

Uncle Clean: That's great to hear! Now, let's say you encounter a situation where you need to incorporate multiple 2FA methods for the same payment method, like adding an authenticator app alongside SMS-based authentication for PayPal. How would you approach this? Additionally, do you believe that solely inheriting from the 2FA classes would be sufficient for your payment methods? I'm referring to the need for additional features to be added to your payment classes, beyond inheriting from the 2FA classes.

Mohammad: Well, there are situations where I could create additional classes to inherit the necessary features for payment methods. However, I'm concerned about the long-term practicality if I keep adding more and more features. Uncle, I would like to hear your thoughts on this matter.

Uncle Clean: In certain scenarios, employing inheritance may not be the most practical or efficient approach to transferring features from one class to another. In such cases, it is advisable to consider the principle of Composition over Inheritance (CoI) as a better alternative.

Mohammad: In simple words, what do we mean by that?

Uncle Clean: Composition over inheritance is a principle in OOP that suggests favoring composition, or building objects by combining simpler components, over inheritance, where objects inherit properties and behaviors from parent classes. With composition, we can combine smaller, modular components for greater flexibility and code reusability. It reduces tight coupling, avoids fragility, and improves code readability and maintainability. Embracing composition will result in more efficient and adaptable code.

Mohammad: Interesting! I will do my best to apply that. Thanks uncle.

After reviewing different examples, Mohammad changed his codebase to the following one: (_Added SMSAuthorizer and created an object in debit card class_)

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
```

Output:
```bash
156
Verifying code 24682
Processing Debit Card payment...
Verifying code: 67891.
```

-------

### 5- Dependency Inversion Principle (DIP)
