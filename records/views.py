from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

# from django.shortcuts import get_object_or_404

# from .models import HealthRecord
# from .serializers import HealthRecordSerializer


@api_view(["POST"])
def create_health_record(request: Request) -> Response:
    return Response({"message": "Health record created!"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_my_history(request: Request) -> Response:
    """Devuelve el historial médico del usuario actual."""
    return Response({"message": "Health record history"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_history(request: Request, user_id: int) -> Response:
    """Devuelve el historial médico de un usuario en específico."""
    return Response({"message": "Health record history"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_summary(request: Request, user_id: int) -> Response:
    """Devuelve un resumen del historial médico de un usuario en específico."""
    return Response({"message": "Health record summary"}, status=status.HTTP_200_OK)
