from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RegistView,
    HomeView,
    CustumLoginView,
    CustumLogoutView,
    BarcodeView,
    BookAddView,
    DetailView,
    MoneyView,
    UserUpdateView,
    PasswordUpdateView,
    PrivacyView,
    UserProfileView,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'life'

urlpatterns = [
    path('regist/', RegistView.as_view(), name='regist'),
    path('login/', CustumLoginView.as_view(), name='login'),
    path('logout/', CustumLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('detail/<uuid:uuid>/', DetailView.as_view(), name='detail'),
    path('barcode/', BarcodeView.as_view(), name='barcode'),
    path('add/', BookAddView.as_view(), name='add'),
    path('money/', MoneyView.as_view(), name='money'),
    path('user_change/', UserUpdateView.as_view(), name='user_change'),
    path('password_change/', PasswordUpdateView.as_view(), name='password_change'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('social-auth/', include('social_django.urls', namespace='social')), # googlelogin
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
