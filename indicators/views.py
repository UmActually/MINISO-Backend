from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404


class HealthIndicatorsView(APIView):
    def post(self, request: Request) -> Response:
        """
        Crea un indicador de salud (no custom).

        Campos:
        - name
        - medical_name (opcional)
        - is_cuantitative
        - is_decimal (en caso de ser cuantitativo)
        - unit_of_measurement (en caso de ser cuantitativo)
        - min (en caso de ser cuantitativo)
        - max (en caso de ser cuantitativo)
        """
        return Response({'message': 'Health indicator created!'}, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        return Response({'message': 'Health indicators'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_custom_health_indicator(request: Request) -> Response:
    """
    Crea un indicador de salud custom.
    TODO: Ver si podremos permitir que los custom sean cuantitativos.

    Campos:
    - name
    - is_cuantitative
    - is_decimal (en caso de ser cuantitativo)
    - unit_of_measurement (en caso de ser cuantitativo)
    - min (en caso de ser cuantitativo)
    - max (en caso de ser cuantitativo)
    """
    return Response({'message': 'Custom health indicator created!'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_suggested_health_indicators(request: Request) -> Response:
    """Devuelve una lista breve de indicadores de salud sugeridos para un usuario."""
    return Response({'message': 'Suggested health indicators'}, status=status.HTTP_200_OK)
