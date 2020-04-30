from rest_framework import generics
from knox import auth
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from user.models import Merchant


class CreateCategory(generics.CreateAPIView)
    """"Create a new category on a website"""
    authentication_classes = (auth.TokenAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        merchant = Merchant.objects.get(user=user)
        serializer.save(merchant=merchant)

