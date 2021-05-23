from django.conf.urls import url
from django.urls import path
from .views import UserRegisterView, UserAccountView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('signup', UserRegisterView.as_view()),
    path('login', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),),
    path('user', UserAccountView.as_view())
]
