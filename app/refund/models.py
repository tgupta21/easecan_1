from django.db import models
from user.models import PaymentApp
from transaction.models import Transaction
from datetime import datetime


class Refund(models.Model):
    """Model for refunds"""
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=25, decimal_places=2)
    reference_id = models.CharField(max_length=100)
    time = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return str(self.pk)


class RefundUrl(models.Model):
    """Storing urls and headers to process refunds"""
    payment_app = models.OneToOneField(PaymentApp, on_delete=models.PROTECT)
    url = models.URLField()
    headers = models.TextField()
