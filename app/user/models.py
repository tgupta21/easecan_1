from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from directory.models import Directory
from core.models import User


COUNTRIES = [
        ('India', 'India'),
    ]

BUSINESS_TYPE = (
    (1, 'Entertainment'),
)


class Shop(models.Model):
    """Adding shops (using mobile apps) user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_area = models.CharField(max_length=255)
    business_pincode = models.CharField(max_length=20)
    business_city = models.CharField(max_length=25)
    business_state = models.CharField(max_length=25)

    business_country = models.CharField(choices=COUNTRIES, max_length=25)

    owner_name = models.CharField(max_length=255)

    business_category = models.PositiveSmallIntegerField(choices=BUSINESS_TYPE)

    pan_or_tin = models.CharField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)

    uid = GenericRelation(Directory)


class Website(models.Model):
    """Adding online website user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=255)
    business_area = models.CharField(max_length=255)
    business_pincode = models.CharField(max_length=20)
    business_city = models.CharField(max_length=25)
    business_state = models.CharField(max_length=25)
    business_country = models.CharField(choices=COUNTRIES, max_length=25)

    website = models.URLField()

    owner_name = models.CharField(max_length=255)
    business_category = models.PositiveSmallIntegerField(choices=BUSINESS_TYPE)

    pan_or_tin = models.CharField(max_length=100, unique=True)

    is_verified = models.BooleanField(default=False)


class Bank(models.Model):
    """Payment apps or banks user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    country = models.CharField(choices=COUNTRIES, max_length=25)

    key = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name
