from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name="task-list"),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]

"""
URL Configuration for Task App.

URL patterns:
- '' (empty path): TaskListView.as_view() - Lists all tasks.
- 'create/': TaskCreateView.as_view() - Creates a new task.
- '<int:pk>/update/': TaskUpdateView.as_view() - Updates an existing task.
- '<int:pk>/delete/': TaskDeleteView.as_view() - Deletes a task.
"""