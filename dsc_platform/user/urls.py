from django.urls import path
from .views import UserRegisterView, UserAccountView
from rest_framework_simplejwt import views as jwt_views

# Important to run unit test
app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path('me/', UserAccountView.as_view(), name='me')
]
