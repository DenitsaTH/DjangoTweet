from django.urls import path

from forecast.api import get_weather_forecast


app_name = 'forecast'

urlpatterns = [
    path('weather/', get_weather_forecast, name='get_weather_forecast'),
]
