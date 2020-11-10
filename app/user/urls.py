from django.urls import path

from .views import CreateUserApi, LoginView, \
    ManageUserView, UserPhotoView, sign_page

app_name = 'user'

urlpatterns = [
    path('api/create/', CreateUserApi.as_view(), name='create'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/me/', ManageUserView.as_view(), name='me'),
    path('api/upload-photo/', UserPhotoView.as_view(), name='upload-photo'),
    path('sign/', sign_page, name='sign'),
]
