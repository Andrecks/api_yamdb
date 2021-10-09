from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories', views.CategoriesViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'titles', views.TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, 'reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', views.CommentViewSet, 'comments')
router.register(r'users', views.UserViewSet)
# router.register(r'follow', FollowViewSet, 'following')

urlpatterns = [
    # path('v1/', include(router.urls)),
    # path('v1/auth', include('djoser.urls')),
    # path('v1/auth', include('djoser.urls.jwt')),
    # path('v1/users/me/', views.UserMeView.as_view(), name='me'),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', views.VerifyEmail.as_view(), name='verify'),    
    path('v1/', include(router.urls)),

]