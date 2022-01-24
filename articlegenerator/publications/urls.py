from django.urls import path

from django.contrib import admin
from . import views


app_name = 'publications'
urlpatterns = [
    path('publish', views.publish, name='publish')
]
