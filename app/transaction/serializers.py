from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import PaymentRequest, Transaction
from directory.models import Directory
from user.models import Merchant, Payer, PaymentApp
from user.serializers import PayerSerializer
from rest_framework import status


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


# class PayeeRelatedField(serializers.RelatedField):
#     """Serializer for payee object in Payment"""
#
#     def to_representation(self, value):
#         if isinstance(value, PaymentRequest):
#             serializer = PaymentRequestSerializer(value)
#         if isinstance(value, Merchant):
#             serializer = MerchantDetailSerializer(value)
#
#         return serializer.data
#
#
# class PaymentAppDetailSerializer(serializers.ModelSerializer):
#     """Serialize the payment app object"""
#
#     class Meta:
#         model = PaymentApp
#         fields = ('id', 'name')
#
#
# class InitiatePaymentSerializer(serializers.ModelSerializer):
#     """Serialize a transaction at initialisation"""
#     uid = serializers.UUIDField(required=True, write_only=True)
#     payee_object = PayeeRelatedField(read_only=True)
#
#     class Meta:
#         model = Transaction
#         fields = ('id', 'uid', 'initialisation_time', 'payee_object', 'status', 'currency', 'amount')
#         read_only_fields = ('initialisation_time', 'payee_object', 'status', 'currency', 'amount')
#
#     def create(self, validated_data):
#         uid = validated_data.pop('uid')
#         directory = Directory.objects.get(uid=uid)
#         payee_object = directory.payee_object
#         if directory.content_type.model == 'PaymentRequest':
#             transaction = Transaction(**validated_data, payee_object=payee_object,
#                                       currency=payee_object.currency, amount=payee_object.amount)
#         transaction.save()
#         return transaction
#
#
# class PaymentDetailSerializer(serializers.ModelSerializer):
#     """Serialize payment details"""
#     payer = PayerSerializer()
#
#     class Meta:
#         model = PaymentDetail
#         fields = ('id', 'currency', 'amount', 'reference_id',
#                   'payment_method', 'completion_time', 'payer', 'comment')
#         read_only_fields = ('completion_time',)
#
#
# class CompletePaymentSerializer(serializers.ModelSerializer):
#     """Serializer for transaction after successful payment"""
#     id = serializers.IntegerField(required=True)
#     payment_detail = PaymentDetailSerializer(required=True)
#     payee_object = PayeeRelatedField(read_only=True)
#
#     class Meta:
#         model = Transaction
#         fields = ('id', 'payment_detail', 'initialisation_time', 'payee_object', 'status', 'is_international')
#         read_only_fields = ('initialisation_time', 'payee_object', 'status', 'is_international')
#
#     def create(self, validated_data):
#         transaction = Transaction.objects.get(id=validated_data.get('id'))
#         payment_detail_data = validated_data.pop('payment_detail')
#         payer_data = payment_detail_data.pop('payer')
#         payer, created = Payer.objects.get_or_create(name=payer_data.get('name'),
#                                                      email=payer_data.get('email'),
#                                                      phone=payer_data.get('phone'))
#         payment_detail = PaymentDetail(**payment_detail_data, payer=payer)
#         payment_detail.save()
#         transaction.payment_detail = payment_detail
#         transaction.status = 2
#         if transaction.payee_object.currency != payment_detail_data.get('currency'):
#             transaction.is_international = True
#         transaction.save()
#         return transaction
