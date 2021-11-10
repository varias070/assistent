from django.urls import path
from . import views
from .views import *

app_name = 'assistant'
urlpatterns = [
    path('', HomePage.as_view(), name='home')
]
