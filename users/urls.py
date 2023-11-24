from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("test/", views.test),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("users/", views.create_patient),
    path("users/doctors/", views.create_doctor),
    path("users/<int:user_id>/", views.UserView.as_view()),
    path("me/", views.CurrentUserView.as_view()),
    path("me/doctor/", views.get_patient_doctor),
    path("me/patients/", views.get_doctor_patients),
]
