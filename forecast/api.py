from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from forecast.services import get_forecast, get_page_content
from forecast.models import CitiesCatalog


@swagger_auto_schema(method='get', tags=['weather'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather_forecast(city: CitiesCatalog):
    """
    get:

    """

    soup = get_page_content(city)
    result = get_forecast(soup)

    return Response(result, status=status.HTTP_200_OK)
