from django.core.mail import EmailMessage


def send_email(mail_subject, message, to_email):
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
