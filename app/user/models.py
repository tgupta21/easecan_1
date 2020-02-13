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

CURRENCY = [
    ('INR', 'INR')
]


class Merchant(models.Model):
    """Adding Merchant user model"""
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

    is_verified = models.BooleanField(default=False)

    website = models.URLField(blank=True, null=True)

    uid = GenericRelation(Directory, related_query_name='merchant')


class Bank(models.Model):
    """Payment apps or banks user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    country = models.CharField(choices=COUNTRIES, max_length=25)

    key = models.CharField(max_length=100, unique=True)
    currency = models.CharField(choices=CURRENCY, max_length=3)

    def __str__(self):
        return self.name
