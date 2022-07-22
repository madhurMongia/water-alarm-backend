from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from .models import newUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, newTokenSerializer


class RegistrationView(APIView):

    def post(self, request):
        serilizer = UserSerializer(data=request.data)
        if serilizer.is_valid():
            account = serilizer.save()
            username = serilizer.validated_data['username']
            token = Token.objects.create(user=account)
            return Response({'msg': "user with username " + username + " created "}, status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = newTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_object_or_404(
                Token, user=serializer.validated_data['user'])
            user.last_login = timezone.now()
            user.save()
            return Response({'key': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
