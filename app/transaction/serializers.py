from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Payment
from directory.models import Directory
from user.models import Merchant


class PayeeFieldSerializer(serializers.RelatedField):
    """Serialize payee_object"""
    def to_representation(self, obj):
        return {
            'id': obj.pk,
            'name': obj.business_name,
        }


class PaymentInitialisationSerializer(serializers.ModelSerializer):
    """Serializer for initialising transaction"""
    payee_object = PayeeFieldSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'uid', 'id', 'payee_object', 'initialisation_time', 'currency', 'status', 'token')
        read_only_fields = (
            'id', 'payee_object', 'initialisation_time', 'currency', 'status', 'token')


class PaymentCompletionSerializer(serializers.ModelSerializer):
    payee_object = PayeeFieldSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ('token', 'uid', 'id', 'payee_object', 'initialisation_time', 'currency', 'status', 'payer',
                  'completion_time', 'payment_currency', 'payment_amount', 'amount', 'payment_method',
                  'reference_number', 'comment')
        read_only_fields = (
            'uid', 'payee_object', 'initialisation_time', 'currency', 'status', 'completion_time')

    def create(self, validated_data):
        return Payment.objects.get(token=validated_data.pop('token'))
