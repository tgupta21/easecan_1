from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import Merchant
from datetime import datetime


class Settlement(models.Model):
    """"model for a settlement request"""
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)
    time = models.DateTimeField(default=datetime.utcnow)
    amount = models.DecimalField(decimal_places=2)
    currency = models.CharField(max_length=3)

    """bank"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    object_id = models.PositiveIntegerField(editable=False, blank=True, null=True)
    bank_object = GenericForeignKey('content_type', 'object_id')

    STATUS_CHOICES = (
        (1, 'failed'),
        (2, 'successful'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)


class IndiaBankAccount(models.Model):
    """"Bank details for India"""
    merchant = models.ManyToManyField(Merchant)
    holder_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)
    account_number = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
