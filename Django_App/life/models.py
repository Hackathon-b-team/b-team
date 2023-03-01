from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    UserManager, AbstractBaseUser, PermissionsMixin,
)
from django.urls import reverse_lazy
from django.utils import timezone
import uuid


class Users(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=100, unique=True, validators=[username_validator])
    email = models.EmailField(max_length=254)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def get_absolute_url(self):
        return reverse_lazy('life:home')
    

class CategoryModel(models.Model):
    uid = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    category_name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class BookBarcodeModel(models.Model):
    barcode =models.CharField(max_length=15)
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    page_count = models.PositiveSmallIntegerField(null=True, blank=True)
    image_link = models.URLField(null=True, blank=True)
    image_path = models.ImageField(upload_to='img/', default='img/noimage.png')
    released_at = models.DateField(null=True, blank=True)
    purchased_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    uid = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    cid = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING)
    bid = models.ForeignKey(BookBarcodeModel, on_delete=models.DO_NOTHING)
    progress = models.PositiveSmallIntegerField(default=0)
    evaluation = models.PositiveSmallIntegerField(default=0)
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bid.title
