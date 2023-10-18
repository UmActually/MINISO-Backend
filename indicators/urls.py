from django.urls import path
from . import views

urlpatterns = [
    path("indicators/", views.HealthIndicatorsView.as_view()),
    path("indicators/custom/", views.create_custom_health_indicator),
    path("indicators/suggested/", views.get_suggested_health_indicators),
]
