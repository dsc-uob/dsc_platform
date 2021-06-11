from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'post'

router = DefaultRouter()
router.register('article', views.ArticleViewset)
router.register('articlecomment', views.ArticleCommentViewset)
router.register('enquiry', views.EnquiryViewset)
router.register('enquirycomment', views.EnquiryCommentViewset)

urlpatterns = [
    path('', include(router.urls)),
]
