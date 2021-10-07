from django.shortcuts import render
from jwt import exceptions
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import datetime as dt
import jwt
from django.conf import settings

class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        user = request.data
        if not User.objects.filter(username=user['username']).exists():
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user)
            email_body = user.username+', твой код активации аккаунта: \n' + str(token)
        else:
            user = User.objects.filter(username=user['username']).get()
            email_body = 'На этот адрес уже был выслан код для активации аккаунта'
            if user.is_verified==True:
                 return VerifyEmail.send_token(user)
            user_data = request.data
                # token = RefreshToken.for_user(user).access_token
                # email_body = user.username+', твой код авторизации: \n' + str(token)

    #RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relative_link = reverse('verify')
        # absurl = 'http://'+current_site+relative_link+'?token='+str(token)

        data = {'email_adress': user.email,
                'email_body': email_body,
                'email_subject': 'Your YaMDB Key'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    pass
    def post(self, request):
        token = request.data['token']
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                token = AccessToken.for_user(user)
                user.save()
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Ваш токен устарел'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.exceptions.DecodeError as e:
            return Response({'error': 'Некорректный токен'},
                            status=status.HTTP_400_BAD_REQUEST)
