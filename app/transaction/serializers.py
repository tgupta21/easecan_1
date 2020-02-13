from abc import ABC

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Transaction
from directory.models import Directory


class PayeeFieldSerializer(serializers.RelatedField):
    """Serialize payee_object"""
    def to_representation(self, obj):
        return {
            'type': obj.user.user_type,
            'id': obj.pk,
            'name': obj.business_name,
        }


class TransactionInitialisationSerializer(serializers.ModelSerializer):
    """Serializer for initialising transaction"""
    uid = serializers.UUIDField(write_only=True)
    key = serializers.CharField(max_length=100, write_only=True)
    payee_object = PayeeFieldSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('uid', 'key', 'id', 'payee_object', 'payer', 'initialisation_time', 'merchant_currency', 'merchant_amount', 'payment_method', 'reference_number', 'order_id', 'status')
        read_only_fields = ('id', 'payee_object', 'payer', 'initialisation_time', 'merchant_currency', 'merchant_amount', 'payment_method', 'reference_number', 'order_id', 'status')

    def create(self, validated_data):
        key = validated_data.pop('key', None)
        uid = validated_data.pop('uid', None)
        transaction = Transaction.start_new_payment(uid=uid, key=key)
        transaction.save()
        return transaction


class TransactionCompletionSerializer(serializers.ModelSerializer):
    """Serializer for completing transaction"""
    key = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Transaction
        fields = ()