from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from directory.models import Directory
from core.models import User


class Shop(models.Model):
    """Adding shops (using mobile apps) user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_area = models.CharField(max_length=255)
    business_pincode = models.CharField(max_length=20, unique=True)
    business_city = models.CharField(max_length=25)
    business_state = models.CharField(max_length=25)
    business_country = models.CharField(max_length=25)

    owner_name = models.CharField(max_length=255)

    SHOP_TYPE = (
        (1, 'Entertainment'),
    )

    business_category = models.PositiveSmallIntegerField(choices=SHOP_TYPE)

    pan_or_tin = models.CharField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)

    uid = GenericRelation(Directory)

    @classmethod
    def create(cls, phone, password, **extra_fields):
        """Creates a new shop"""
        user = User.objects.create_user(phone, password, user_type=2)
        return cls(user=user, **extra_fields)


class Website(models.Model):
    """Adding online website user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=255)
    business_area = models.CharField(max_length=255)
    business_pincode = models.CharField(max_length=20, unique=True)
    business_city = models.CharField(max_length=25)
    business_state = models.CharField(max_length=25)
    business_country = models.CharField(max_length=25)

    website = models.URLField()

    owner_name = models.CharField(max_length=255)

    BUSINESS_TYPE = (
        (1, 'Entertainment'),
    )

    business_category = models.PositiveSmallIntegerField(choices=BUSINESS_TYPE)

    pan_or_tin = models.CharField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)

    @classmethod
    def create(cls, phone, password, **extra_fields):
        """Creates a new shop"""
        user = User.objects.create_user(phone, password, user_type=3)
        return cls(user=user, **extra_fields)


class Bank(models.Model):
    """Payment apps or banks user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    country = models.CharField(max_length=25)

    key = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, phone, password, **extra_fields):
        """Creates a new shop"""
        user = User.objects.create_user(phone, password, user_type=4)
        return cls(user=user, **extra_fields)
