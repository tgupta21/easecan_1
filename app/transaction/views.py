from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import PaymentRequest
from user.models import PaymentApp, Merchant
from directory.models import Directory
from datetime import datetime
from rest_framework.exceptions import APIException


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
            raise APIException('your account is not active')


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
