from django.urls import path

from forecast.api import get_forecast


app_name = 'forecast'

urlpatterns = [
    path('weather/', get_forecast, name='get_forecast'),
]
