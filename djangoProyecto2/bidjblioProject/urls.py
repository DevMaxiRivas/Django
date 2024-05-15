from django.urls import path, include

urlpatterns = [
    # ...
    # path("catalogo/admin/", include("admin.site.urls")),
    path("catalogo/", include("catalogo.urls")),
]
