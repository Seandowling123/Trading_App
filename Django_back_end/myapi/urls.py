from django.urls import path
from . import views

# TradingBotProj1 directory
# python manage.py runserver

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
]