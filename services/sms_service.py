from django.conf import settings
from twilio.rest import Client


def send_twilio_message(body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    return client.messages.create(
        body=body,
        to=settings.DEFAULT_TO_NUMBER,
        from_=settings.TWILIO_PHONE_NUMBER
    )
