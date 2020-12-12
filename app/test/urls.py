from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DSC Platform Rest API",
        default_version='v0.4',
        description="An documentations for DSC Platform Rest API.",
        contact=openapi.Contact(email="muhmdhsn313@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    url(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='json'),
    url('', schema_view.with_ui('swagger', cache_timeout=0), name='doc'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
