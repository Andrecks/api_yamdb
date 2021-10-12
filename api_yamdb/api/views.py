# from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import models
# from rest_framework import pagination
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, filters, mixins
from . import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .utils import Util
from media.models import Categories, Genres, Titles, Review, Comment
from users.permissions import IsAdmin
from users.permissions import (
    IsAdminOrReadOnly, IsAuthorOrNotSimpleUserReadOnly
)
import jwt
from django.conf import settings


class RetrieveUpdate(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    pass


class SignUpView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer

    def post(self, request):
        user_data = request.data
        if not User.objects.filter(username=user_data['username']).exists():
            serializer = self.serializer_class(data=user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = default_token_generator.make_token(user)
        else:
            # user = User.objects.filter(username=user_data['username']).get()
            # token = default_token_generator.make_token(user)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        email_body = user.username + ', твой код активации аккаунта: \n' + str(token)
        if user.is_verified == True:
            email_body = 'На этот адрес уже был выслан код для активации аккаунта'
            # token = AccessToken.for_user(user)
            # email_body = user.username+', твой токен: \n' + str(token)
            user_data = request.data

        data = {'email_adress': user.email,
                'email_body': email_body,
                'email_subject': 'Авторизация на YaMDB'}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):

    def post(self, request):
        token = request.data['token']
        user = get_object_or_404(User, username=request.data['username'])
        if default_token_generator.check_token(user, token):
            if not user.is_verified:
                user.is_verified = True
                user.save()
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.GetUserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name',]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        actions = ['create', 'partial_update']
        if self.action in actions:
            return serializers.PostTitleSerializer
        return serializers.GetTitleSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    model = Review
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrNotSimpleUserReadOnly,
    )
    authentication_classes = (JWTAuthentication,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title.pk)

    def perform_create(self, serializer):
        get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrNotSimpleUserReadOnly,
    )
    model = Comment
    authentication_classes = (JWTAuthentication,)
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return Comment.objects.filter(review=review.pk)

    def perform_create(self, serializer):
        get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user)


class UserMeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = serializers.UserMeSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = serializers.UserMeSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
