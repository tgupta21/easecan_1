from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from knox.auth import TokenAuthentication


class AuthTokenView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except:
            pass
        token = Token.objects.create(user=user)
        token.save()
        return Response(token.key, status=status.HTTP_201_CREATED)
