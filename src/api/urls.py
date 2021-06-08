from os import name
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import UserCreate

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('account/create/', UserCreate),
]
