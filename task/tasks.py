from celery_app import app
from django.core.mail import send_mail
from django.conf import settings

email_host_user = settings.EMAIL_HOST_USER

@app.task
def send_email_task(subject, message, recipient_list):
    send_mail(subject, message, email_host_user, recipient_list)
