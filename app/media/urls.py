from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ImageViewSet

app_name = 'media'

router = DefaultRouter()
router.register('image', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
