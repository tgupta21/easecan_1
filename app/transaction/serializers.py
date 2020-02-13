from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Transaction
from directory.models import Directory
from user.models import Merchant


class PayeeFieldSerializer(serializers.RelatedField):
    """Serialize payee_object"""
    def to_representation(self, obj):
        return {
            'id': obj.pk,
            'name': obj.business_name,
        }


class TransactionInitialisationSerializer(serializers.ModelSerializer):
    """Serializer for initialising transaction"""
    payee_object = PayeeFieldSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'uid', 'id', 'payee_object', 'initialisation_time', 'currency', 'amount', 'status')
        read_only_fields = (
            'id', 'payee_object', 'initialisation_time', 'currency', 'amount', 'status')

    def create(self, validated_data):
        uid = validated_data.get('uid', None)
        directory = Directory.objects.get(uid=uid)
        if directory.payee_object.user.user_type == 2:
            return Transaction.start_new_payment(uid=uid)


class TransactionCompletionSerializer(serializers.ModelSerializer):
    """Serializer for completing transaction"""
    key = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Transaction
