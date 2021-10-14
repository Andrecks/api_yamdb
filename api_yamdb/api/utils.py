import os

from django.core.mail import EmailMessage


class Util:

    @staticmethod
    def send_email(data):
        msg = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            to=(data['email_adress'],),
        )
        msg.send()
