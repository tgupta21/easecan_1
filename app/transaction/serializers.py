from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import PaymentRequest, Transaction, CurrencyConverter
from directory.models import Directory
from user.models import Merchant, Payer, PaymentApp
from user.serializers import PayerSerializer
from rest_framework import status
from .currency_converter import payment_value
from datetime import datetime
from rest_framework.exceptions import APIException


class MerchantDetailSerializer(serializers.ModelSerializer):
    """Serializer to show merchant details"""

    class Meta:
        model = Merchant
        fields = ('id', 'business_name', 'website', 'business_country')


class PaymentRequestSerializer(serializers.ModelSerializer):
    """Serializer for payment request"""
    merchant = MerchantDetailSerializer(read_only=True)

    class Meta:
        model = PaymentRequest
        fields = ('id', 'merchant', 'order_id', 'currency', 'amount', 'time')
        read_only_fields = ('merchant', 'time',)

    def create(self, validated_data):
        payment_request = PaymentRequest(**validated_data)
        payment_request.save()
        directory = Directory.create(payee=payment_request,
                                     name=payment_request.merchant.business_name + ': ' + payment_request.order_id)
        directory.save()
        return payment_request


class CurrencyConverterSerializer(serializers.ModelSerializer):
    """serializer to convert currency by the payment app"""

    class Meta:
        model = CurrencyConverter
        fields = ('currency', 'amount', 'payment_currency', 'payment_amount', 'key')
        read_only_fields = ('payment_amount', 'key')

    def create(self, validated_data):
        payment_app = validated_data.pop('payment_app')
        payment_amount = payment_value(**validated_data)
        currency_converter = CurrencyConverter(payment_app=payment_app, payment_amount=payment_amount,
                                               **validated_data)
        currency_converter.save()
        return currency_converter


class PayeeRelatedField(serializers.RelatedField):
    """Serializer for payee object in Payment"""

    def to_representation(self, value):
        if isinstance(value, PaymentRequest):
            serializer = PaymentRequestSerializer(value)
        if isinstance(value, Merchant):
            serializer = MerchantDetailSerializer(value)

        return serializer.data


class PaymentAppDetailSerializer(serializers.ModelSerializer):
    """Serialize the payment app object"""

    class Meta:
        model = PaymentApp
        fields = ('id', 'name')


class InitiatePaymentSerializer(serializers.ModelSerializer):
    """Serialize a transaction at initialisation"""
    # payee_object = PayeeRelatedField(read_only=True)
    merchant = MerchantDetailSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'uid', 'display_name', 'initialisation_time', 'merchant', 'currency', 'amount')
        read_only_fields = ('display_name', 'initialisation_time', 'merchant', 'currency', 'amount')

    def create(self, validated_data):
        directory = Directory.objects.get(uid=validated_data.get('uid'))
        display_name = directory.display_name

        if isinstance(directory.payee_object, Merchant):
            merchant = directory.payee_object
            transaction = Transaction(merchant=merchant, display_name=display_name, currency=merchant.currency,
                                      **validated_data)
        if isinstance(directory.payee_object, PaymentRequest):
            payment_request = directory.payee_object
            merchant = payment_request.merchant
            currency = payment_request.currency
            amount = payment_request.amount
            transaction = Transaction(merchant=merchant, display_name=display_name, currency=currency,
                                      amount=amount, **validated_data)

        transaction.save()
        return transaction


class CompletePaymentSerializer(serializers.ModelSerializer):
    """Serializer for transaction after successful payment"""
    id = serializers.IntegerField(required=True)
    payer = PayerSerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'uid', 'display_name', 'initialisation_time', 'merchant', 'currency', 'amount', 'key',
                  'payment_currency', 'payment_amount', 'payment_reference_id', 'payment_method', 'payment_comment',
                  'payer', 'completion_time', 'is_international')
        read_only_fields = ('uid', 'display_name', 'initialisation_time', 'merchant', 'amount', 'currency',
                            'payment_currency', 'completion_time', 'is_international')

    def create(self, validated_data):
        transaction = Transaction.objects.get(id=validated_data.get('id'))
        payer_data = validated_data.pop('payer')
        payer, created = Payer.objects.get_or_create(name=payer_data.get('name'),
                                                     email=payer_data.get('email'),
                                                     phone=payer_data.get('phone'))

        payment_amount = validated_data.get('payment_amount')

        if validated_data.get('key') is None:
            if transaction.amount is None:
                transaction.amount = payment_amount
            else:
                if transaction.amount != payment_amount:
                    raise APIException('payment amount not valid')

            transaction.payment_currency = transaction.currency
            transaction.payment_amount = validated_data.get('payment_amount')

        else:
            converter = CurrencyConverter.objects.get(key=validated_data.get('key'))
            transaction.key = validated_data.get('key')
            
            if transaction.amount is None:
                if converter.currency == transaction.currency:
                    transaction.amount = converter.amount
                    transaction.payment_currency = converter.payment_currency
                    transaction.payment_amount = converter.payment_amount
                    transaction.is_international = True
                else:
                    raise APIException('invalid key')
            else:
                if converter.amount == transaction.amount and converter.currency == transaction.currency:
                    transaction.payment_currency = converter.payment_currency
                    transaction.payment_amount = converter.payment_amount
                    transaction.is_international = True
                else:
                    raise APIException('invalid key')

        transaction.payment_reference_id = validated_data.get('payment_reference_id')
        transaction.payment_method = validated_data.get('payment_method')
        transaction.payment_comment = validated_data.get('payment_comment')
        transaction.completion_time = datetime.utcnow()
        transaction.payer = payer
        transaction.status = 2
        transaction.save()
        return transaction
