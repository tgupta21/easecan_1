from rest_framework import generics, authentication, mixins, permissions, status
from .serializers import TransactionInitialisationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from user.models import Bank, Merchant
from directory.models import Directory


class InitiatePayment(generics.CreateAPIView, mixins.CreateModelMixin):
    """Initiating a new payment"""
    serializer_class = TransactionInitialisationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        bank = Bank.objects.get(user=user)
        serializer.save(bank=bank)
