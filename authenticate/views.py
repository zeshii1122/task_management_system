from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    """Render the home page."""
    def get(self, request):
        return render(request, 'authenticate/home.html')


class LoginView(View):
    """Render the login page and authenticate users."""
    def get(self, request):
        return render(request, 'authenticate/login.html')

    def post(self, request):
        """Handle POST request to authenticate users."""
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('task-list')
        else:
            messages.warning(request, "Username or Password is incorrect !!")
            return redirect('login')


class LogoutView(View):
    """Logout the user and redirect to the home page."""
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('home')


class RegisterView(FormView):
    """Render the registration page and handle user registration."""
    template_name = 'authenticate/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Save the form data and authenticate the user."""
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class EditProfileView(LoginRequiredMixin, FormView):
    """Render the edit profile page and handle profile updates."""
    template_name = 'authenticate/edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        """Add the current user instance to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Save the form data and display success message."""
        form.save()
        messages.success(self.request, "Profile Updated Successfully")
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    """Render the change password page and handle password changes."""
    template_name = 'authenticate/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        """Add the current user instance to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Save the new password and update the session hash."""
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Password Changed Successfully")
        return super().form_valid(form)
