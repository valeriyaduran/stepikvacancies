from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.forms import UserRegisterForm, UserLoginForm


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
