from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Directory
from user.models import Merchant
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateStaticDirectory


class StaticDirectoryViewSet(viewsets.ModelViewSet):
    """Manage Static UID in Directory"""
    serializer_class = CreateStaticDirectory
    queryset = Directory.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        """Create a new Directory"""
        user = self.request.user
        payee_object = Merchant.objects.get(user=user)
        serializer.save(payee_object=payee_object)

    def get_queryset(self):
        """Retrieve the directory of authenticated Merchant"""
        return self.queryset.filter(merchant__user=self.request.user)
