from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a test task
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task.',
            created_by=self.user,
            assigned_user=self.user
        )

    def test_task_list_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the task list view
        response = self.client.get(reverse('task-list'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the task is present in the response context
        self.assertIn('tasks', response.context)
        self.assertQuerysetEqual(
            response.context['tasks'],
            [repr(self.task)],
            transform=str
        )

    def test_task_create_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the task create view
        response = self.client.post(
            reverse('task-create'),
            {
                'title': 'New Test Task',
                'description': 'This is a new test task.',
                'assigned_user': self.user.id
            }
        )

        # Check if the task is created successfully
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Check if the task exists in the database
        new_task = Task.objects.filter(title='New Test Task').first()
        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.assigned_user, self.user)

    def test_task_update_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the task update view
        response = self.client.post(
            reverse('task-update', kwargs={'pk': self.task.pk}),
            {
                'title': 'Updated Test Task',
                'description': 'This is an updated test task.',
                'assigned_user': self.user.id
            }
        )

        # Check if the task is updated successfully
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

        # Refresh the task from the database
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.title, 'Updated Test Task')
        self.assertEqual(updated_task.description, 'This is an updated test task.')

    def test_task_delete_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the task delete view
        response = self.client.post(reverse('task-delete', kwargs={'pk': self.task.pk}))

        # Check if the task is deleted successfully
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion

        # Check if the task is deleted from the database
        task_exists = Task.objects.filter(pk=self.task.pk).exists()
        self.assertFalse(task_exists)
