from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from directory.models import Directory
from transaction.models import Transaction


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('user must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email address"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'shops'),
        (3, 'websites'),
        (4, 'banks'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)


class Shop(models.Model):
    """Adding shops (using mobile apps) user model"""
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=4)
    mobile_number = models.IntegerField(unique=True)
    
    shop_name = models.CharField(max_length=255)
    shop_address = models.CharField(max_length=255)
    shop_area = models.CharField(max_length=255)
    shop_pincode = models.CharField(max_length=20, unique=True)
    shop_city = models.CharField(max_length=25)
    shop_state = models.CharField(max_length=25)
    shop_country = models.CharField(max_length=25)

    owner_name = models.CharField(max_length=255)

    SHOP_TYPE = (
        (1, 'Entertainment'),
    )

    shop_category = models.PositiveSmallIntegerField(choices=SHOP_TYPE)

    pan_or_tin = models.CharField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)

    qr_code = GenericRelation(Directory)


class Website(models.Model):
    """Adding online website user model"""
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=4)
    mobile_number = models.IntegerField(unique=True)
    business_name = models.CharField(max_length=100)
    website = models.URLField()

    owner_name = models.CharField(max_length=255)

    BUSINESS_TYPE = (
        (1, 'Entertainment'),
    )

    shop_category = models.PositiveSmallIntegerField(choices=BUSINESS_TYPE)

    pan_or_tin = models.CharField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)

    qr_code = GenericRelation(Directory)


class Bank(models.Model):
    """Payment apps or banks user model"""
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4)

    def __str__(self):
        return self.name
