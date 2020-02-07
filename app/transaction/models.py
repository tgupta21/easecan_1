from django.db import models
from core.models import User, Bank
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from directory.models import Directory


class TransactionManager(models.Manager):

    def payment_initialisation(self, uid, token):
        """initialising payment"""
        directory = Directory.objects.get(uid=uid)

        if directory.is_active:
            payee = directory.payee_object
            bank = Bank.objects.get(token=token)

            if not self.filter(uid=payee):
                """new transaction"""
                transaction = self.model(payee_object=payee, bank=bank)
                transaction.save(using=self._db)
            else:
                """pending transaction"""
                transaction = self.filter(uid=payee)

            return transaction
        else:
            raise ValueError('Not an active uid')

    def payment_completion(self, token, id, **kwargs):
        """payment is successful"""
        transaction = self.filter(id=id)
        bank = Bank.objects.get(token=token)

        if transaction.bank == bank or "":
            transaction.update(**kwargs, status=3)
            transaction.save(using=self._db)
        else:
            raise ValueError('not authorised')

        return transaction


class Transaction(models.Model):
    """Storing all the transactions"""
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, default="")

    """Payee"""
    payee_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    payee_object = GenericForeignKey('payee_type', 'object_id')

    customer = models.CharField(max_length=100)

    initialisation_time = models.DateTimeField(auto_now=True)
    completion_time = models.DateTimeField(default="")
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=25, decimal_places=2, default="")
    payment_method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100, default="")
    international = models.BooleanField(default=False)

    STATUS_CHOICES = (
        (1, 'initiated'),
        (2, 'pending'),
        (3, 'successful'),
        (4, 'refunded'),
        (5, 'failed'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    detail = models.CharField(max_length=255, default="")
    uid = GenericRelation(Directory)

    objects = TransactionManager()

    def __str__(self):
        return self.pk

