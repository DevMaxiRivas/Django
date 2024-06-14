from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # ...
    path("register/", views.register, name="register"),
    path(
        "assign-role/<str:username>/",
        views.assign_role_to_user,
        name="assign_role_to_user",
    ),
    path("test/", views.test_view, name="test_view"),
]
