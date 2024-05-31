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
    # Formularios
    # Generos
    path("generos/", views.genero_list, name="generos"),
    path("genero/new/", views.genero_new, name="genero_new"),
    path("genero/update/<pk>", views.genero_update, name="genero_update"),
    # Autores
    path("autores2/", views.autor_list, name="autores2"),
    path("autores2/new/", views.autor_new, name="autor_new"),
    path("autores2/update/<pk>", views.autor_update, name="autor_update"),
    # Ejemplares
    path("ejemplares/", views.ejemplar_list, name="ejemplares"),
    path("ejemplares/new/", views.ejemplar_new, name="ejemplar_new"),
    path("ejemplares/update/<pk>", views.ejemplar_update, name="ejemplar_update"),
    # Idiomas
    path("idiomas/", views.idioma_list, name="idiomas"),
    path("idiomas/delete/<pk>", views.idioma_delete, name="idioma_delete"),
]
