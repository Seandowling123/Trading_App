from django.urls import path
from . import views

# Django_back_end directory
# python manage.py runserver
# sudo python3 manage.py runserver 0.0.0.0:8000

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('asdf/', views.asdf),
    path('historical_data/<str:ticker>', views.historical_data),
    path('index/', views.index)
]