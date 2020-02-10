from rest_framework import serializers
from .models import Transaction
from directory.models import Directory


class InitiatePayment(serializers.ModelSerializer):
    """send uid to initiate payment"""

    class Meta:
        model = Directory
        fields = ('uid', )
        read_only_fields = ('uid', )


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction objects"""

    class Meta:
        model = Transaction
        fields = ('id', )