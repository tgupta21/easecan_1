from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from directory.models import Directory
from core.models import User
from phonenumber_field.modelfields import PhoneNumberField


COUNTRIES = [
        ('India', 'India'),
    ]

BUSINESS_TYPE = (
    (1, 'Entertainment'),
)


class Merchant(models.Model):
    """Adding Merchant user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=255)
    business_area = models.CharField(max_length=255)
    business_pincode = models.IntegerField()
    business_city = models.CharField(max_length=25)
    business_state = models.CharField(max_length=25)

    business_country = models.CharField(choices=COUNTRIES, max_length=25)

    owner_name = models.CharField(max_length=50)

    business_category = models.PositiveSmallIntegerField(choices=BUSINESS_TYPE)

    is_verified = models.BooleanField(default=False)

    website = models.URLField(blank=True, null=True)

    uid = GenericRelation(Directory, related_query_name='merchant')


class PaymentApp(models.Model):
    """Payment apps or banks user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Payer(models.Model):
    """Details of person paying, provided by payment app"""
    name = models.CharField(max_length=50)
    phone = PhoneNumberField()

    def __str__(self):
        return str(self.phone)


class Customer(models.Model):
    """Details of customer of merchant"""
    name = models.CharField(max_length=50)
    phone = PhoneNumberField()

    def __str__(self):
        return str(self.phone)
