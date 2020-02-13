from django.db import models
from user.models import Bank
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
import datetime

from directory.models import Directory


class Transaction(models.Model):
    """Storing all the transactions"""
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, blank=True, null=True)

    """Payee"""
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    payee_object = GenericForeignKey('content_type', 'object_id')

    payer = models.CharField(max_length=100, blank=True, null=True)  # by bank

    initialisation_time = models.DateTimeField(default=datetime.datetime.utcnow)
    completion_time = models.DateTimeField(blank=True, null=True)

    currency = models.CharField(max_length=3)  # by merchant
    amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)  # by merchant

    payment_currency = models.CharField(max_length=3, blank=True)  # by bank
    payment_amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)  # by bank

    payment_method = models.CharField(max_length=50, blank=True, null=True)   # by bank
    reference_number = models.CharField(max_length=100, blank=True, null=True)  # by bank

    uid = models.UUIDField()

    STATUS_CHOICES = (
        (1, 'initiated'),
        (2, 'successful'),
        (3, 'failed'),
        (4, 'refund initiated'),
        (5, 'refunded')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def start_new_payment(cls, uid):
        """New transaction request by bank"""
        directory = Directory.objects.get(uid=uid)
        payee = directory.payee_object
        currency = payee.currency
        return cls(payee_object=payee, status=1, uid=uid, currency=currency)
