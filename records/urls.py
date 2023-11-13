from django.urls import path
from . import views

urlpatterns = [
    path("records/", views.create_health_record),
    path("records/history/", views.get_my_history),
    path("records/<int:record_id>/", views.delete_health_record),
    path("users/<int:user_id>/history/", views.get_user_history),
    path("users/<int:user_id>/summary/", views.get_user_summary)
]
