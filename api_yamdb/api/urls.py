from django.urls import include, path
from . import views

urlpatterns = [
    # path('v1/', include(router.urls)),
    # path('v1/auth', include('djoser.urls')),
    # path('v1/auth', include('djoser.urls.jwt')),
    path('v1/auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', views.VerifyEmail.as_view(), name='verify'),
]