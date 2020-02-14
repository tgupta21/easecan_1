from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import PaymentRequest
from directory.models import Directory
from user.models import Merchant, Payer, Customer
from user.serializers import CustomerSerializer, PayerSerializer


class PaymentRequestSerializer(serializers.ModelSerializer):
    """Serializer for payment request"""
    customer = CustomerSerializer()

    class Meta:
        model = PaymentRequest
        fields = ('id', 'order_id', 'currency', 'amount', 'description', 'customer')

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        if Customer.objects.get(phone=customer_data.get('phone'), name=customer_data.get('name')):
            customer = Customer.objects.get(phone=customer_data.get('phone'), name=customer_data.get('name'))
        else:
            customer = CustomerSerializer.create(CustomerSerializer(), validated_data=customer_data)
            customer.save()
        payment_request = PaymentRequest(**validated_data, customer=customer)
        payment_request.save()
        directory = Directory.create(payee=payment_request,
                                     name=payment_request.merchant.business_name + ': ' + payment_request.order_id)
        directory.save()
        return payment_request
