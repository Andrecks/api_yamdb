# from django.shortcuts import render
from django.contrib.auth import models
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, filters
from jwt import exceptions
from . import serializers
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# from .serializers import UserSerializer, CategorySerializer, GenreSerializer
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .utils import Util
from media.models import Categories, Genres, Titles, Review, Comment
from users.permissions import CategoryGenreTitlePermission, ReviewPermission, UserPermission, CommentPermission
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# import datetime as dt
import jwt
from django.conf import settings

class SignUpView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    
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
                token = AccessToken.for_user(user)
                email_body = user.username+', твой токен: \n' + str(token)
            user_data = request.data

        data = {'email_adress': user.email,
                'email_body': email_body,
                'email_subject': 'Авторизация на YaMDB'}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.GetUserSerializer
    permission_classes = (UserPermission,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('username',)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (CategoryGenreTitlePermission,)
    authentication_classes = (JWTAuthentication,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (CategoryGenreTitlePermission,)
    authentication_classes = (JWTAuthentication,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (CategoryGenreTitlePermission,)
    authentication_classes = (JWTAuthentication,)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    model = Review
    permission_classes = (ReviewPermission,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title.pk)

    def perform_create(self, serializer):
        get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (CommentPermission,)
    model = Comment
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return Comment.objects.filter(rewview=review.pk)

    def perform_create(self, serializer):
        get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user)