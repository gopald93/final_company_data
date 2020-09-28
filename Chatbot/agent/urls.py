from django.urls import path
from agent.views import *
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('conversations/', conversations, name='conversations'),
    ]