# custom_filters.py

from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def format_datetime(value):
    if isinstance(value, datetime):
        # Format datetime as desired (e.g., "Jan 1, 2022 12:00 PM")
        return value.strftime("%b %d, %Y %I:%M %p")
    return value