from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .models import HealthIndicator
from .serializers import HealthIndicatorSerializer, CustomHealthIndicatorSerializer


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
        data = request.data
        serializer = HealthIndicatorSerializer(data=data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"message": "Health indicator created!"}, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        """
        Devuelve todos los indicadores de salud predeterminados,
        más los custom del usuario.
        """
        indicators = HealthIndicator.objects.filter(
            Q(added_by=None) | Q(added_by=request.user)
        )
        serializer = HealthIndicatorSerializer(indicators, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
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
    data = request.data
    serializer = CustomHealthIndicatorSerializer(data=data, many=False)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    return Response({"message": "Custom health indicator created!"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_suggested_health_indicators(request: Request) -> Response:
    """Devuelve una lista breve de indicadores de salud sugeridos para un usuario."""
    
    # TODO: tomar los 4 indicadores más frecuentes para el usuario
    
    return Response({"message": "Suggested health indicators"}, status=status.HTTP_200_OK)
