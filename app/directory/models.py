from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid


class Directory(models.Model):
    """QR codes directory for linking them"""
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    """Foreign Key to payee"""
    payee_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    payee_object = GenericForeignKey('payee_type', 'object_id')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uid)

    @classmethod
    def create(cls, payee):
        """Create a new directory"""
        return cls(payee_object=payee)
