import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import User, UserRole


def user_exists_in_db(request: Request) -> bool:
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    if not authorization_header:
        return False
    _, token = authorization_header.split(' ')
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload['user_id']
    return User.objects.filter(id=user_id).exists()


class IsPatient(BasePermission):
    def has_permission(self, request: Request, view):
        return user_exists_in_db(request) and request.user.role == UserRole.PATIENT


class IsDoctor(BasePermission):
    def has_permission(self, request: Request, view):
        return user_exists_in_db(request) and request.user.role == UserRole.DOCTOR


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return user_exists_in_db(request) and \
            (request.user.role == UserRole.ADMIN or request.user.is_staff)
