from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentSetView

app_name = 'post_sys'

router = DefaultRouter()
router.register('posts', PostViewSet, )
router.register('comments', CommentSetView, )

urlpatterns = [
    path('', include(router.urls)),
]
