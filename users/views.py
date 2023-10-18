from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
def test(_request: Request) -> Response:
    return Response({'message': 'Hello world!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request: Request) -> Response:
    """
    Crea un usuario (paciente).

    Campos:
    - email
    - password
    - first_names
    - last_names
    - birth_date
    - height
    - phone_number (opcional)
    - medical_history (opcional)
    """
    data = request.data
    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response({'message': 'User created!'}, status=status.HTTP_201_CREATED)


class UserView(APIView):
    def get(self, _request: Request, user_id: int) -> Response:
        """Devuelve un usuario en específico, dado el ID. Solo para administradores."""
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, user_id: int) -> Response:
        """Actualiza un usuario en específico, dado el ID. Solo para administradores."""
        if 'password' in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)

        updated_user = serializer.save()

        resp_serializer = UserSerializer(updated_user)
        return Response(resp_serializer.data, status=status.HTTP_200_OK)

    def delete(self, _request: Request, user_id: int) -> Response:
        """Elimina un usuario en específico, dado el ID. Solo para administradores."""
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
