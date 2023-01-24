from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)
from django.urls import reverse_lazy
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('life:home')
    

class CategoryModel(models.Model):
    uid = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    category_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class BookBarcodeModel(models.Model):
    barcode =models.CharField(max_length=15, unique=True)
    barcode_image = models.ImageField(upload_to='barcode/')
    title = models.CharField(max_length=100)
    auther = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    page_count = models.SmallIntegerField(null=True, blank=True)
    image_link = models.ImageField(upload_to='img/', null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    uid = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    cid = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING)
    bid = models.ForeignKey(BookBarcodeModel, on_delete=models.DO_NOTHING)
    progress = models.CharField(max_length=10, default='unread')
    evaluation = models.PositiveSmallIntegerField(default=0)
    review = models.TextField(null=True, blank=True)
    purchased_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bid.title


class UserIconModel(models.Model):
    uid = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    icon_image = models.ImageField(upload_to='icon/')
    active_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.icon_image
