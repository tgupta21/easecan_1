from django.db import models
from core.models import User, Bank
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Transaction(models.Model):
    """Storing all the transactions"""
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)

    payee_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    payee = GenericForeignKey('content_type', 'object_id')

    customer = models.CharField(max_length=100)

    initialisation_time = models.DateTimeField
    completion_time = models.DateTimeField
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100)

    STATUS_CHOICES = (
        (1, 'initiated'),
        (2, 'pending'),
        (3, 'successful'),
        (4, 'refunded'),
        (5, 'failed'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    detail = models.CharField(max_length=255)

    def __str__(self):
        return self.transaction_id
