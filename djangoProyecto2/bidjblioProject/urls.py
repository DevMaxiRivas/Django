from django.contrib import admin
from django.urls import path, include

# Recursos muestra de imagenes
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
    path("catalogo/admin/", admin.site.urls),
    path("catalogo/", include("catalogo.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
