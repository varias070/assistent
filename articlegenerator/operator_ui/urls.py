from django.urls import path

from django.contrib import admin
from articles import views
from articles.views import *


app_name = 'articles'
urlpatterns = [
    # path('', admin.site.urls, name='home')
]
