from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet

app_name = 'post_sys'

router = DefaultRouter()
router.register('posts', PostViewSet, )

urlpatterns = [
    path('', include(router.urls)),
]
