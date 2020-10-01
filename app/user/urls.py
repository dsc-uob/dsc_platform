from django.urls import path

from .views import CreateUserApi, LoginView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserApi.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', ManageUserView.as_view(), name='me')
]
