from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating or updating Task model objects.
    This form is based on the Task model and includes specific fields.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'assigned_user', 'status']