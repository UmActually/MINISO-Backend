from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404

from users.models import User, UserRole
from users.permissions import IsPatient, IsAdminOrDoctor
from .models import HealthRecord
from .serializers import group_records_by_date, HealthRecordDeserializer


@api_view(["POST"])
@permission_classes([IsPatient])
def create_health_record(request: Request) -> Response:
    """
    Crea un nuevo registro.

    Campos:
    - health_indicator_id
    - value
    - note (opcional)
    """
    data = request.data
    serializer = HealthRecordDeserializer(data=data, context={"request": request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({"message": "Health record created!"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsPatient])
def delete_health_record(request: Request, record_id: int) -> Response:
    """Elimina un registro."""
    record = get_object_or_404(HealthRecord, id=record_id)

    if record.user != request.user:
        return Response({"message": "You can't delete this health record"}, status=status.HTTP_403_FORBIDDEN)

    record.delete()
    return Response({"message": "Health record deleted!"}, status=status.HTTP_200_OK)


def handle_get_history(user: User, request: Request) -> Response:
    records = HealthRecord.objects.filter(user=user).order_by('-date')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(records, request)
    grouped_data = group_records_by_date(page)
    return paginator.get_paginated_response(grouped_data)


@api_view(["GET"])
@permission_classes([IsPatient])
def get_my_history(request: Request) -> Response:
    """Devuelve el historial médico del usuario actual."""
    return handle_get_history(request.user, request)


@api_view(["GET"])
@permission_classes([IsAdminOrDoctor])
def get_user_history(request: Request, user_id: int) -> Response:
    """Devuelve el historial médico de un usuario en específico."""
    user = request.user
    patient = get_object_or_404(User, id=user_id)
    if user.role == UserRole.DOCTOR and patient.doctor != user:
        return Response(
            {"message": "You can't access this user's health record"},
            status=status.HTTP_403_FORBIDDEN)
    return handle_get_history(patient, request)


@api_view(["GET"])
@permission_classes([IsAdminOrDoctor])
def get_user_summary(request: Request, user_id: int) -> Response:
    """Devuelve un resumen del historial médico de un usuario en específico."""
    user = request.user
    patient = get_object_or_404(User, id=user_id)
    if user.role == UserRole.DOCTOR and patient.doctor != user:
        return Response(
            {"message": "You can't access this user's health record"},
            status=status.HTTP_403_FORBIDDEN)

    # TODO: Implementar con lo que necesite el cliente

    return Response({"message": "Health record summary"}, status=status.HTTP_200_OK)
