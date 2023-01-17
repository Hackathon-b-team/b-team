from django.contrib import admin
from django.urls import path, include
from .views import loginfunc

app_name = 'life'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginfunc, name='login'),
]