from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('api_app.urls')),
]