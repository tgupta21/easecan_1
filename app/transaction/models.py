import uuid
from django.db import models
from user.models import PaymentApp, Merchant, Payer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime
from uuid import uuid4
from directory.models import Directory


class PaymentRequest(models.Model):
    """"Model for one time payment requested by merchant"""
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(decimal_places=2, max_digits=25)
    time = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return str(self.pk)


class Transaction(models.Model):
    """Storing all the transactions/payments"""
    uid = models.UUIDField()
    display_name = models.CharField(max_length=50)

    payment_app = models.ForeignKey(PaymentApp, on_delete=models.PROTECT)
    initialisation_time = models.DateTimeField(default=datetime.utcnow)

    """payee"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    object_id = models.PositiveIntegerField(editable=False, blank=True, null=True)
    payee_object = GenericForeignKey('content_type', 'object_id')

    STATUS_CHOICES = (
        (1, 'initiated'),
        (2, 'successful'),
        (3, 'failed'),
        (4, 'refund initiated'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)

    currency = models.CharField(max_length=3, blank=True, null=True)
    amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)

    key = models.UUIDField(blank=True, null=True)
    payment_currency = models.CharField(max_length=3, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    payment_reference_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_comment = models.CharField(max_length=255, blank=True, null=True)
    payer = models.ForeignKey(Payer, on_delete=models.PROTECT, blank=True, null=True)
    completion_time = models.DateTimeField(blank=True, null=True)

    is_international = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class CurrencyConverter(models.Model):
    """Storing all currency conversion request"""
    time = models.DateTimeField(default=datetime.utcnow)
    payment_app = models.ForeignKey(PaymentApp, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    payment_currency = models.CharField(max_length=3)
    payment_amount = models.DecimalField(max_digits=25, decimal_places=2)
    key = models.UUIDField(default=uuid4)
