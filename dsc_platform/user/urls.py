from django.conf.urls import url
from .views import RegisterView, UserProfileView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    url(r'^signup', RegisterView.as_view()),
    url(r'^login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'),

    url(r'^user', UserProfileView.as_view())
]
