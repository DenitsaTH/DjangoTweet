from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from forecast.services import get_forecast, get_page_content


@swagger_auto_schema(
    method='get',
    tags=['weather'],
    manual_parameters=[
        openapi.Parameter(
            'city',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            enum=[
                'Sofia',
                'Plovdiv',
                'Varna',
                'Burgas',
                'Ruse',
                'Stara Zagora',
                'Pleven',
                'Dobrich',
                'Shumen',
                'Montana',
            ],
        ),
    ],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather_forecast(request):
    """
    get:

    """
    city = request.GET.get('city').lower()
    city = ''.join(city.split())
    soup = get_page_content(city)
    result = get_forecast(soup)

    return Response(result, status=status.HTTP_200_OK)
