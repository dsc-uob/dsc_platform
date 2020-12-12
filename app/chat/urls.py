from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'chat'

router = DefaultRouter()
router.register('message', views.ChatMessageView, )
router.register('role', views.ChatRoleView, )

urlpatterns = [
    path('create/', views.CreateChatSessionView.as_view(), name='create'),
    path('session/', views.ListChatSessionView.as_view(), name='session'),
    path('session/<str:pk>/', views.ManageChatSessionView.as_view(),
         name='session/<str>'),
    path('', include(router.urls)),
]
