from django.urls import path, include
from .views import (
    RegistView, HomeView, CustumLoginView, CustumLogoutView, BarcodeView,
    BookregistView,
)

app_name = 'life'

urlpatterns = [
    path('regist/', RegistView.as_view(), name='regist'),
    path('login/', CustumLoginView.as_view(), name='login'),
    path('logout/', CustumLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('barcode/', BarcodeView.as_view(), name='barcode'),
    path('book_regist/', BookregistView.as_view(), name='book_regist'),
    path('social-auth/', include('social_django.urls', namespace='social')), # googlelogin
]