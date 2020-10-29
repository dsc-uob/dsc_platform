from django.urls import path
from .views import coming_soon

app_name = 'core'

urlpatterns = [
    path('', coming_soon, name='home'),
]
