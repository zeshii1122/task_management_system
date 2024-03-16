from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticateViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        # Set up the client
        self.client = Client()

    def test_home_view(self):
        # Access the home view
        response = self.client.get(reverse('home'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/home.html')

    def test_login_view(self):
        # Access the login view (GET request)
        response = self.client.get(reverse('login'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/login.html')

        # Login with valid credentials (POST request)
        login_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), login_data, follow=True)

        # Check if the user is redirected to the task list page after login
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('task-list'))

    def test_logout_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the logout view
        response = self.client.get(reverse('logout'), follow=True)

        # Check if the user is redirected to the home page after logout
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))

    def test_register_view(self):
        # Access the register view (GET request)
        response = self.client.get(reverse('register'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/register.html')

        # Register a new user (POST request)
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(reverse('register'), register_data, follow=True)

        # Check if the user is redirected to the home page after registration
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))

        # Check if the new user is created
        new_user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(new_user)

    def test_edit_profile_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the edit profile view (GET request)
        response = self.client.get(reverse('edit-profile'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/edit_profile.html')

        # Edit the profile (POST request)
        edit_data = {'first_name': 'Updated', 'last_name': 'User'}
        response = self.client.post(reverse('edit-profile'), edit_data, follow=True)

        # Check if the profile is updated
        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'User')

    def test_change_password_view(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the change password view (GET request)
        response = self.client.get(reverse('change-password'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/change_password.html')

        # Change the password (POST request)
        password_data = {'old_password': 'testpassword', 'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(reverse('change-password'), password_data, follow=True)

        # Check if the password is changed
        updated_user = User.objects.get(username='testuser')
        self.assertTrue(updated_user.check_password('newpassword123'))

        # Logout to test new password
        self.client.logout()
        login_data = {'username': 'testuser', 'password': 'newpassword123'}
        response = self.client.post(reverse('login'), login_data, follow=True)
        self.assertRedirects(response, reverse('task-list'))

