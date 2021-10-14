from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoriesViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'titles', views.TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                'reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<id>\d+)/comments',
                views.CommentViewSet, 'comments')
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('v1/users/me/', views.UserMeView.as_view(), name='me'),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', views.VerifyEmail.as_view(), name='verify'),
    path('v1/', include(router.urls)),

]
