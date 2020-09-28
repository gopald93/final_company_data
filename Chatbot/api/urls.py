from django.urls import path
from api.views import *

urlpatterns = [
    path('api_methods/', api_methods, name='api_methods'),
    ]

  