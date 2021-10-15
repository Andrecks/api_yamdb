from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from media.models import Category, Genres
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review, Title
from users.models import User
from users.permissions import (GenreCategoryPermission, IsAdmin,
                               IsAdminOrReadOnly,
                               IsAuthorOrNotSimpleUserReadOnly)

from . import serializers
from .filters import TitleFilter
from .mixins import GenreCategoryMixin
from .utils import Util


class SignUpView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        if not User.objects.filter(username=username).exists():
            serializer.save()
            user = User.objects.get(email=user_data['email'])
            token = default_token_generator.make_token(user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        email_body = (f'{user.username}, твой код активации аккаунта:'
                      + str(token))
        if user.is_verified is True:
            email_body = 'На этот адрес уже был выслан код активации аккаунта'
            user_data = request.data

        data = {'email_adress': user.email,
                'email_body': email_body,
                'email_subject': 'Авторизация на YaMDB'}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):
    def post(self, request):
        serializer = serializers.UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = request.data['confirmation_code']
            user = get_object_or_404(User, username=request.data['username'])
            if default_token_generator.check_token(user, token):
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                token = AccessToken.for_user(user)
                return Response({'token': str(token)},
                                status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.GetUserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'get':
            if request.user.is_authenticated:
                serializer = serializers.UserMeSerializer(request.user)
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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


class CategoriesViewSet(GenreCategoryMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (GenreCategoryPermission,)
    authentication_classes = (JWTAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GenreCategoryMixin):
    queryset = Genres.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (GenreCategoryPermission,)
    authentication_classes = (JWTAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        actions = ['create', 'partial_update']
        if self.action in actions:
            return serializers.PostTitleSerializer
        return serializers.GetTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrNotSimpleUserReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrNotSimpleUserReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review.objects.prefetch_related('comments'),
            id=self.kwargs.get('id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('id')
        )
        serializer.save(author=self.request.user, review=review)
