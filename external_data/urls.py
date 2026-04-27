from django.urls import path
from . import views

urlpatterns = [
    path('pogoda/', views.weather_view, name='weather'),
]