from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import MerchantSerializer, AuthTokenSerializer


class MerchantSignupView(generics.CreateAPIView):
    """Creating a new user in the system"""
    serializer_class = MerchantSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
