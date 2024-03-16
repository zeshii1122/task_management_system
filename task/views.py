from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import send_email_task

from . import forms
from . import models



class TaskListView(LoginRequiredMixin, ListView):
    """
    View for listing tasks.

    Attributes:
        login_url (str): URL to redirect to for login.
        model (Model): Django model to use for the view.
        template_name (str): HTML template for rendering the view.
        context_object_name (str): Name of the context object containing tasks.

    Methods:
        get_queryset(self): Returns the queryset of tasks based on user permissions and filters.
    """
    login_url = '/login/'
    model = models.Task
    template_name = 'task/list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """
        Get the queryset of tasks based on user permissions and filters.

        Returns:
            QuerySet: Filtered queryset of tasks.
        """
        # Get all tasks
        queryset = super().get_queryset()

        # Filter tasks based on current user's ownership or assignment
        user = self.request.user
        if user.is_authenticated:
            from django.db.models import Q

            # Assuming `user` is the user for whom you want to filter tasks
            queryset = queryset.filter(Q(created_by=user) | Q(assigned_user=user))

            # Filter by status if status filter is provided
            status_filter = self.request.GET.get('status', None)
            if status_filter:
                queryset = queryset.filter(status=status_filter)
        else:
            # Return an empty queryset for anonymous users
            queryset = queryset.none()

        return queryset


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new task.
    Attributes:
        login_url (str): URL to redirect to for login.
        model (Model): Django model to use for the view.
        template_name (str): HTML template for rendering the view.
        form_class (Form): Form class for creating tasks.
        success_url (str): URL to redirect to after successful form submission.
    Methods:
        form_valid(self, form): Sets the created_by field to the current user.
    """
    login_url = '/login/'
    model = models.Task
    template_name = 'task/add_task.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        """
        Set the created_by field to the current user.
        Args:
            form (Form): Form instance representing the new task.
        Returns:
            HttpResponse: Response after form submission.
        """
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Get the assigned user's email
        assigned_user = form.cleaned_data.get('assigned_user')
        if assigned_user and assigned_user.email:
            subject = 'New Task Assigned'
            message = f'A new task has been assigned to you.'
            recipient_list = [assigned_user.email]
            send_email_task.delay(subject, message, recipient_list)
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing task.
    Attributes:
        login_url (str): URL to redirect to for login.
        model (Model): Django model to use for the view.
        template_name (str): HTML template for rendering the view.
        form_class (Form): Form class for updating tasks.
        success_url (str): URL to redirect to after successful form submission.
    """
    login_url = '/login/'
    model = models.Task
    template_name = 'task/add_task.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Get the assigned user's email
        assigned_user = form.cleaned_data.get('assigned_user')
        if assigned_user and assigned_user.email:
            subject = 'Task Updated'
            message = f'An existing task has been updated and assigned to you.'
            recipient_list = [assigned_user.email]
            send_email_task.delay(subject, message, recipient_list)

        return response



class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a task.
    Attributes:
       login_url (str): URL to redirect to for login.
       model (Model): Django model to use for the view.
       template_name (str): HTML template for rendering the view.
       success_url (str): URL to redirect to after successful deletion.
    """
    login_url = '/login/'
    model = models.Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
