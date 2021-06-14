from os import name
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import UserCreate, Login

urlpatterns = [
    path('login/', Login.as_view()),
    path('account/create/', UserCreate.as_view()),
]
