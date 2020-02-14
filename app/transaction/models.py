import uuid
from django.db import models
from user.models import PaymentApp, Merchant, Payer, Customer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
import datetime

from directory.models import Directory


class PaymentRequest(models.Model):
    """"Model for one time payment requested by merchant"""
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(decimal_places=2, max_digits=25)
    description = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.pk)


class Transaction(models.Model):
    """Storing all the transactions"""
    initialisation_time = models.DateTimeField(default=datetime.datetime.utcnow)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    completion_time = models.DateTimeField(blank=True, null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)

    STATUS_CHOICES = (
        (1, 'initiated'),
        (2, 'successful'),
        (3, 'failed'),
        (4, 'refund initiated'),
        (5, 'refunded')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return str(self.pk)


class Payment(models.Model):
    """Payment details provided by payment app"""
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT)
    payment_app = models.ForeignKey(PaymentApp, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    payer = models.ForeignKey(Payer, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.pk)