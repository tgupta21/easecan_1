from django.db import models
from user.models import Bank
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from directory.models import Directory


class Transaction(models.Model):
    """Storing all the transactions"""
    transaction_id = models.IntegerField(primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, blank=True, null=True)

    """Payee"""
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    payee_object = GenericForeignKey('content_type', 'object_id')

    payer = models.CharField(max_length=100, blank=True, null=True)  # by bank

    initialisation_time = models.DateTimeField(auto_now=True)
    completion_time = models.DateTimeField(blank=True, null=True)

    merchant_currency = models.CharField(max_length=3)  # by merchant
    merchant_amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)  # by merchant

    payment_currency = models.CharField(max_length=3, blank=True)  # by bank
    payment_amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)  # by bank

    payment_method = models.CharField(max_length=50, blank=True, null=True)   # by bank
    reference_number = models.CharField(max_length=100, blank=True, null=True)  # by bank

    international = models.BooleanField(default=False)

    order_id = models.CharField(max_length=50, blank=True, null=True)  # by merchant
    customer = models.CharField(max_length=100, blank=True, null=True)  # by merchant

    STATUS_CHOICES = (
        (1, 'initiated'),
        (2, 'payment initiated'),
        (3, 'successful'),
        (4, 'failed'),
        (5, 'refund initiated'),
        (6, 'refunded')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    detail = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def start_new_payment(cls, uid, key):
        """New transaction request by bank"""
        directory = Directory.objects.get(uid=uid)
        payee = directory.payee_object
        bank = Bank.objects.get(key=key)
        currency = bank.currency
        return cls(payee_object=payee, bank=bank, status=2, payment_currency=currency)

    @classmethod
    def initiate_new_transaction(cls, payee, currency, amount, order_id="", customer=""):  # payee=user
        """New Transaction request by merchant"""
        return cls(payee_object=payee, merchant_currency=currency, merchant_amount=amount, order_id=order_id,
                   customer=customer)
