from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, phone, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(phone=phone, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, email=""):
        """Creates and saves a new super user"""
        user = self.create_user(phone, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.user_type = 1
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with phone address"""
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    USER_TYPE_CHOICES = (
        (0, 'unspecified'),
        (1, 'admin'),
        (2, 'merchant'),
        (3, 'bank'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=0)

    def __str__(self):
        return str(self.phone)
