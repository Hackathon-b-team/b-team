from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from .forms import RegistForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# @login_required
class HomeView(TemplateView):
    template_name = 'home.html'

class RegistView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm


# class LoginView(LoginView):
#     template_name = 'login.html'
#     authentication_form = LoginForm

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # next_url = request.POST['next']
        # if user is not None and user.is_active:
        #     login(request, user)
        # if next_url:
        #     return redirect(next_url)
        return redirect('life:home')


class LogoutView(LogoutView):
    pass


