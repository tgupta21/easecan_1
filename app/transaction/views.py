from rest_framework import generics, authentication, mixins, permissions, status, viewsets
from rest_framework.response import Response
from .serializers import PaymentInitialisationSerializer, PaymentCompletionSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from user.models import Bank, Merchant
from directory.models import Directory
from datetime import datetime
from rest_framework.exceptions import APIException


class InitiatePaymentView(generics.CreateAPIView, mixins.UpdateModelMixin):
    """Initiating a new payment"""
    serializer_class = PaymentInitialisationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Initiate a new payment with authenticated bank"""
        user = self.request.user
        bank = Bank.objects.get(user=user)
        uid = self.request.data['uid']
        directory = Directory.objects.get(uid=uid)
        payee = directory.payee_object
        currency = payee.currency
        if directory.payee_object.user.user_type == 2:
            serializer.save(bank=bank, payee_object=payee, status=1, uid=uid, currency=currency)


class PaymentCompletionView(generics.CreateAPIView):
    serializer_class = PaymentCompletionSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        bank = Bank.objects.get(user=user)
        serializer_data = self.request.data
        payment = Payment.objects.get(token=serializer_data['token'])
        if payment.status == 1:
            if payment.bank == bank:
                payment.completion_time = datetime.utcnow()
                payment.payer = serializer_data['payer']
                payment.payment_currency = serializer_data['payment_currency']
                payment.payment_amount = serializer_data['payment_amount']
                payment.amount = serializer_data['amount']
                payment.payment_method = serializer_data['payment_method']
                payment.reference_number = serializer_data['reference_number']
                payment.comment = serializer_data['comment']
                payment.status = 2
                payment.save()
                return serializer.save()

        else:
            raise APIException('not authorised')
