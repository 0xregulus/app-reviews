from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authy.serializers import UserSerializer

User = get_user_model()


class AuthView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data.get('username'))
            if user.check_password(request.data.get('password')):
                return Response(UserSerializer(user).data)
            else:
                return Response({'password': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
