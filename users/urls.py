from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("test/", views.test),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("users/", views.create_user),
    path("users/<int:user_id>/", views.UserView.as_view()),
    path("me/", views.CurrentUserView.as_view()),
]
