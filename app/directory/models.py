from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid


class DirectoryManager(models.Manager):

    def get_uid(self, payee):
        """get uid for given payee"""
        directory = self.model(content_object=payee)
        return str(directory.uid)


class Directory(models.Model):
    """QR codes directory for linking them"""
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    """Foreign Key to payee"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    is_active = models.BooleanField(default=True)

    objects = DirectoryManager()

    def __str__(self):
        return str(self.uid)

    @classmethod
    def create(cls, payee):
        """Create a new directory"""
        return cls(content_object=payee)
