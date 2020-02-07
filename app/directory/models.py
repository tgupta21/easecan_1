from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid


class DirectoryManager(models.Manager):

    def create_directory(self, payee_object):
        """Create a new directory"""
        directory = self.model(payee_object=payee_object)
        directory.save(using=self._db)

        return directory


class Directory(models.Model):
    """QR codes directory for linking them"""
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    """Foreign Key to payee"""
    payee_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    payee_object = GenericForeignKey('payee_type', 'object_id')

    objects = DirectoryManager()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.uid
