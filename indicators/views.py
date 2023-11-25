from typing import Any

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count, Q

from users.permissions import IsPatient, IsAdmin
from .models import HealthIndicator
from .serializers import HealthIndicatorSerializer, HealthIndicatorDeserializer, CustomHealthIndicatorDeserializer


class HealthIndicatorsView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def post(self, request: Request) -> Response:
        """
        Crea un indicador de salud (no custom). Solo para administradores.

        Campos:
        - name
        - medical_name (opcional)
        - is_cuantitative
        - is_decimal (en caso de ser cuantitativo)
        - min (en caso de ser cuantitativo)
        - max (en caso de ser cuantitativo)
        - unit_of_measurement (opcional, en caso de ser cuantitativo)
        """
        data = request.data
        serializer = HealthIndicatorDeserializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_indicator = serializer.save()

        resp_serializer = HealthIndicatorSerializer(new_indicator)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        """
        Devuelve todos los indicadores de salud predeterminados,
        más los custom del usuario.
        """
        indicators = HealthIndicator.objects.filter(
            Q(added_by=None) | Q(added_by=request.user)
        ).order_by("added_by", "id")
        serializer = HealthIndicatorSerializer(indicators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdmin])
def bulk_create_health_indicators(request: Request) -> Response:
    """
    Crea varios indicadores de salud (no custom) a partir de un archivo CSV.
    Solo para administradores.
    """
    file: InMemoryUploadedFile = request.FILES.get("file")
    if not file:
        return Response({"message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    def evaluate(expression: str) -> Any:
        if expression.isdigit():
            return int(expression)
        if expression.isnumeric():
            return float(expression)
        if expression == "TRUE":
            return True
        if expression == "FALSE":
            return False
        return expression

    content = file.read().decode("utf-8")
    csv_lines = content.split("\r\n")
    indicators = []

    headers = csv_lines.pop(0).split(",")
    for row in csv_lines:
        kwargs = {
            key: evaluate(value)
            for key, value in zip(headers, row.split(",")) if value
        }
        kwargs.setdefault("is_decimal", False)
        kwargs.setdefault("min", 1)
        kwargs.setdefault("max", 10)
        indicators.append(HealthIndicator(**kwargs))

    HealthIndicator.objects.bulk_create(indicators)
    return Response({"message": "Health indicators created"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsPatient])
def create_custom_health_indicator(request: Request) -> Response:
    """
    Crea un indicador de salud custom.

    Campos:
    - name
    """
    data = request.data
    serializer = CustomHealthIndicatorDeserializer(data=data, context={"request": request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    new_indicator = serializer.save()

    resp_serializer = HealthIndicatorSerializer(new_indicator)
    return Response(resp_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsPatient])
def get_suggested_health_indicators(request: Request) -> Response:
    """Devuelve una lista breve de indicadores de salud sugeridos para un usuario."""

    indicators = HealthIndicator.objects.annotate(
        count=Count("records", filter=Q(records__user_id=request.user.id))
    ).order_by("-count")[:4]

    serializer = HealthIndicatorSerializer(indicators, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
