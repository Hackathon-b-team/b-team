from django.urls import path
from .views import (
    RegistView, HomeView, CustumLoginView, CustumLogoutView, BarcodeView
)

app_name = 'life'

urlpatterns = [
    path('regist/', RegistView.as_view(), name='regist'),
    path('login/', CustumLoginView.as_view(), name='login'),
    path('logout/', CustumLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('barcode/', BarcodeView.as_view(), name='barcode'),
]