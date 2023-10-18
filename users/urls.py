from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test),
    path('users/', views.create_user),
    path('users/<int:user_id>/', views.UserView.as_view())
]
