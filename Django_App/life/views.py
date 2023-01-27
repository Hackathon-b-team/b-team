from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from .forms import RegistForm, LoginForm, BarcodeUpdateForm, BarcodeInputForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# SignUp用
class RegistView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


# login用
class CustumLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


# logout用
class CustumLogoutView(LogoutView):
    pass


# home用
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


# バーコード用
class BarcodeView(LoginRequiredMixin, FormView):
    template_name = 'barcode.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        context = super().get_context_data(**kwargs)
        context.update({
            'barcode_update_form': BarcodeUpdateForm(**self.get_form_kwargs()),
            'barcode_input_form': BarcodeInputForm(**self.get_form_kwargs()),
        })
        return context

    def post(self, request, *args, **kwargs):
        # バーコードアップデート用
        if 'form_send_barcode_update' in request.POST:
            updateform = BarcodeUpdateForm(**self.get_form_kwargs())
            # バリデーション
            if updateform.is_valid():          
                return self.form_valid(updateform)
            else:
                return self.form_invalid(updateform)
        # バーコードインプット用
        elif 'form_send_barcode_input' in request.POST:
            inputform = BarcodeInputForm(**self.get_form_kwargs())
            # バリデーション
            if inputform.is_valid():
                return self.form_valid(inputform)
            else:
                return self.form_invalid(inputform)
