from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from users.models import User
from indicators.models import HealthIndicator
from .models import HealthRecord
from .serializers import HealthRecordSerializer, HealthRecordInputSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_health_record(request: Request) -> Response:
    """
    Crea un nuevo registro.

    Campos:
    - health_indicator_id
    - value
    - note (opcional)
    """
    data = request.data
    serializer = HealthRecordInputSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    health_indicator_id = validated_data["health_indicator_id"]

    # Validar que el indicador exista
    health_indicator = get_object_or_404(HealthIndicator, id=health_indicator_id)

    # Validar que el usuario tenga permiso para agregar registros de este indicador
    if health_indicator.is_custom and health_indicator.added_by != request.user:
        return Response(
            {"message": "You can't add records to this indicator"},
            status=status.HTTP_403_FORBIDDEN)

    # Validar que el valor esté dentro del rango
    value = validated_data["value"]
    if not (health_indicator.min <= value <= health_indicator.max):
        return Response(
            {"message": "Value out of range"},
            status=status.HTTP_400_BAD_REQUEST)

    HealthRecord.objects.create(
        user=request.user,
        health_indicator=health_indicator,
        **validated_data
    )

    return Response({"message": "Health record created!"}, status=status.HTTP_201_CREATED)


def handle_get_history(user: User, request: Request) -> Response:
    records = HealthRecord.objects.filter(user=user).order_by('-date')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(records, request)
    serializer = HealthRecordSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_history(request: Request) -> Response:
    """Devuelve el historial médico del usuario actual."""
    return handle_get_history(request.user, request)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_user_history(request: Request, user_id: int) -> Response:
    """Devuelve el historial médico de un usuario en específico."""
    user = get_object_or_404(User, id=user_id)
    return handle_get_history(user, request)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_user_summary(request: Request, user_id: int) -> Response:
    """Devuelve un resumen del historial médico de un usuario en específico."""

    # TODO: Implementar con lo que necesite el cliente

    return Response({"message": "Health record summary"}, status=status.HTTP_200_OK)
