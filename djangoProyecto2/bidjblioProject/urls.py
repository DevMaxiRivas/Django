from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ...
    # path("catalogo/admin/", admin.site.urls),
    path("catalogo/", include("catalogo.urls")),
]
