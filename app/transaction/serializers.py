from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import PaymentRequest, Payment
from directory.models import Directory
from user.models import Merchant, Payer
from user.serializers import PayerSerializer


class MerchantDetailSerializer(serializers.ModelSerializer):
    """Serializer to show merchant details"""
    class Meta:
        model = Merchant
        fields = ('id', 'business_name', 'website')


class PaymentRequestSerializer(serializers.ModelSerializer):
    """Serializer for payment request"""
    merchant = MerchantDetailSerializer(read_only=True)

    class Meta:
        model = PaymentRequest
        fields = ('id', 'merchant', 'order_id', 'currency', 'amount', 'description','time')
        read_only_fields = ('merchant', 'time',)

    def create(self, validated_data):
        payment_request = PaymentRequest(**validated_data)
        payment_request.save()
        directory = Directory.create(payee=payment_request,
                                     name=payment_request.merchant.business_name + ': ' + payment_request.order_id)
        directory.save()
        return payment_request


class PayeeRelatedField(serializers.RelatedField):
    """Serializer for payee object in Payment"""
    def to_representation(self, value):
        if isinstance(value, PaymentRequest):
            serializer = PaymentRequestSerializer(value)
        if isinstance(value, Merchant):
            serializer = MerchantDetailSerializer(value)

        return serializer.data


class InitiatePaymentSerializer(serializers.ModelSerializer):
    """Serialize a transaction"""
    uid = serializers.UUIDField(required=True, write_only=True)
    payee_object = PayeeRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'uid', 'initialisation_time', 'payee_object', 'status')
        read_only_fields = ('initialisation_time', 'payee_object', 'status')

    def create(self, validated_data):
        uid = validated_data.pop('uid')
        directory = Directory.objects.get(uid=uid)
        payee_object = directory.payee_object
        payment = Payment(**validated_data, payee_object=payee_object)
        payment.save()
        return payment
