from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import UserSerializer, PatientDeserializer, DoctorDeserializer
from .permissions import IsAdmin


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request: Request) -> Response:
    """Endpoint de prueba."""
    user = request.user
    serializer = UserSerializer(user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_patient(request: Request) -> Response:
    """
    Crea un usuario paciente.

    Campos:
    - email
    - password
    - first_names
    - last_names
    - doctor_id
    - birth_date (formato: YYYY-MM-DD)
    - height (opcional)
    - phone_number (opcional)
    - medical_history (opcional)
    """
    data = request.data
    serializer = PatientDeserializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    new_user = serializer.save()

    return Response({
        "message": "User created!",
        "token": str(AccessToken.for_user(new_user))
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAdmin])
def create_doctor(request: Request) -> Response:
    """
    Crea un usuario doctor.

    Campos:
    - email
    - password
    - first_names
    - last_names
    - phone_number (opcional)
    """
    data = request.data
    serializer = DoctorDeserializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    new_user = serializer.save()

    return Response({
        "message": "User created!",
        "token": str(AccessToken.for_user(new_user))
    }, status=status.HTTP_201_CREATED)


def handle_get_user(user: User) -> Response:
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


def handle_put_user(user: User, request: Request) -> Response:
    if "password" in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(instance=user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors)

    updated_user = serializer.save()

    resp_serializer = UserSerializer(updated_user)
    return Response(resp_serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAdmin]

    def get(self, _request: Request, user_id: int) -> Response:
        """Devuelve un usuario en específico, dado el ID. Solo para administradores."""
        return handle_get_user(get_object_or_404(User, id=user_id))

    def put(self, request: Request, user_id: int) -> Response:
        """Actualiza un usuario en específico, dado el ID. Solo para administradores."""
        return handle_put_user(get_object_or_404(User, id=user_id), request)

    def delete(self, _request: Request, user_id: int) -> Response:
        """Elimina un usuario en específico, dado el ID. Solo para administradores."""
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Devuelve el usuario autenticado."""
        return handle_get_user(request.user)

    def put(self, request: Request) -> Response:
        """Actualiza el usuario autenticado."""
        return handle_put_user(request.user, request)
