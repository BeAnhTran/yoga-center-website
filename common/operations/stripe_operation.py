from django.conf import settings
import stripe


class StripeOperation:
  def __init__(self, name, email, phone, amount, stripeToken, description):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    self.name = name
    self.email = email
    self.phone = phone
    self.amount = amount
    self.stripeToken = stripeToken
    self.description = description

  def call(self):
    customer = self.__create_customer()
    charge = self.__charge(customer)
    return charge

  def __create_customer(self):
    return stripe.Customer.create(
        name=self.name,
        email=self.email,
        phone=self.phone,
        source=self.stripeToken
    )

  def __charge(self, customer):
    return stripe.Charge.create(
        amount=self.amount,
        currency='vnd',
        description=self.description,
        customer=customer.id
    )
