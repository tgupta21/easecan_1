from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import MerchantSerializer, KnoxAuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import login


class MerchantSignupView(generics.CreateAPIView):
    """Creating a new user in the system"""
    serializer_class = MerchantSerializer


# class CreateTokenView(ObtainAuthToken):
#     """Create new auth token for user"""
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LoginView(KnoxLoginView, CreateAPIView):
    """Login token for merchant"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = KnoxAuthTokenSerializer

    def post(self, request, format=None):
        serializer = KnoxAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
