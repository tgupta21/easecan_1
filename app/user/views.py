from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import ShopSerializers, AuthTokenSerializer


class CreateShopView(generics.CreateAPIView):
    """Creating a new user in the system"""
    serializer_class = ShopSerializers


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageShopView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = ShopSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
