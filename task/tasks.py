# tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, recipient_list):
    send_mail(subject, message, 'your@example.com', recipient_list)
