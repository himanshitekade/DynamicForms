from django.urls import path
from application import views
from .views import *



urlpatterns = [
    path('', views.JsonFormConfiguration.as_view(), name='json-config'),
]