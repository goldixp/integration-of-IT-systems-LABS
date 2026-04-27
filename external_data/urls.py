from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_view, name='weather'),
    path('posts/<int:user_id>/', views.posts_view, name='posts'),
    path('api/weather-summary/', views.weather_summary_api, name='weather_summary_api'),
]