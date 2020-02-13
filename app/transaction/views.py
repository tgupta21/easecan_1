from rest_framework import generics, authentication, permissions, status
from .serializers import TransactionInitialisationSerializer
from rest_framework.permissions import IsAuthenticated


class InitiatePayment(generics.CreateAPIView):
    """Creating a new user in the system"""
    serializer_class = TransactionInitialisationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
