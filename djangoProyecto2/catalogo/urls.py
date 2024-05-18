from django.urls import path
from catalogo import views

urlpatterns = [
    # Desarrollando Home
    path("", views.index, name="index"),
    # Planilla para Vista de Lista de Libros
    path("libros/", views.LibroListView.as_view(), name="libros"),
    path("autores/", views.AutorListView.as_view(), name="autores"),
    # Plantilla de Detalle
    path("libro/<pk>", views.LibroDetailView.as_view(), name="libro"),
    path("autor/<pk>", views.AutorDetailView.as_view(), name="autor"),
]
