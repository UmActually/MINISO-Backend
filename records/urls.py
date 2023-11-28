from django.urls import path
from . import views

urlpatterns = [
    path("records/", views.create_health_record),
    path("records/bulk/", views.bulk_create_health_records),
    path("records/history/", views.get_my_history),
    path("records/indicators/<int:indicator_id>/history/", views.get_my_indicator_history),
    path("records/<int:record_id>/", views.delete_health_record),
    path("users/<int:user_id>/history/", views.get_user_history),
    path("users/<int:user_id>/indicators/<int:indicator_id>/history/", views.get_user_indicator_history),
    path("users/<int:user_id>/summary/", views.get_user_summary)
]
