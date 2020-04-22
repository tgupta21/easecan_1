from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import PaymentRequest, Transaction
from user.models import PaymentApp, Merchant
from rest_framework.exceptions import APIException
import requests
import json


class PaymentRequestView(generics.CreateAPIView):
    """make payment request view"""
    serializer_class = serializers.PaymentRequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        merchant = Merchant.objects.get(user=user)
        if merchant.is_active:
            serializer.save(merchant=merchant)
        else:
            raise APIException('invalid request')


class InitiatePaymentView(generics.CreateAPIView):
    """View to initiate a payment"""
    serializer_class = serializers.InitiatePaymentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        payment_app = PaymentApp.objects.get(user=user)
        if payment_app.is_active:
            serializer.save(payment_app=payment_app)
        else:
            raise APIException('your account is not active')


class CompletePaymentView(generics.CreateAPIView):
    """View to complete payment request by payment app"""
    serializer_class = serializers.CompletePaymentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        payment_app = PaymentApp.objects.get(user=user)
        transaction = Transaction.objects.get(id=self.request.data['id'])
        if transaction.payment_app == payment_app:
            if transaction.status == 1:
                serializer.save()
            else:
                raise APIException('you cannot complete this transaction')
        else:
            raise APIException('you are not authorised')
