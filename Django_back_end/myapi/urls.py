from django.urls import path
from . import views
from django.urls import re_path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon_custom.ico', permanent=True)

# Django_back_end directory
# python manage.py runserver
# sudo python3 manage.py runserver 0.0.0.0:8000

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    path('hello-world/', views.hello_world, name='hello_world'),
    path('asdf/', views.asdf),
    path('historical_data/<str:ticker>', views.historical_data),
    path('trade_history/', views.trade_history),
    path('account_details/', views.account_details),
    path('index/', views.index),
]