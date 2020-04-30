from django.db import models
from user.models import Merchant


class Category(models.Model):
    """request details for quick request"""
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    TYPE_CHOICES = (
        (1, 'any_amount'),      # ideal for prepaid recharges
        (2, 'fixed_amount'),    # ideal for physical bills
        (3, 'fetch_amount'),    # ideal for bill payments
    )

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    fetch_url = models.URLField(default="")  # only for fetch_amount type
    fetch_headers = models.TextField(default="")

    confirmation_url = models.URLField()
    confirmation_headers = models.TextField()


class AnyAmountObject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    payee = models.CharField(max_length=100)


class FixedAmountObject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    payee = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2)


class FetchAmountObject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    payee = models.CharField(max_length=100)
