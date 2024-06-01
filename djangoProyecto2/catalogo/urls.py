from django.urls import path
from catalogo import views

urlpatterns = [
    # Desarrollando Home
    path("", views.index, name="index"),
    # Planilla para Vista de Lista de Libros
    path("libros/", views.LibroListView.as_view(), name="libros"),
    path("libros/new/", views.libro_new, name="libro_new"),
    path("libros/update/<pk>", views.libro_update, name="libro_update"),
    path("libros/delete/<pk>", views.libro_delete, name="libro_delete"),
    # Plantilla de Detalle
    path("libro/<pk>", views.LibroDetailView.as_view(), name="libro"),
    # Generos
    # path("generos/", views.genero_list, name="generos"),
    path("generos/", views.GeneroListView.as_view(), name="generos"),
    path("generos/new/", views.genero_new, name="genero_new"),
    path("generos/update/<pk>", views.genero_update, name="genero_update"),
    path("generos/delete/<pk>", views.genero_delete, name="genero_delete"),
    # Autores
    path("autores/", views.AutorListView.as_view(), name="autores"),
    path("autores/new/", views.autor_new, name="autor_new"),
    path("autores/update/<pk>", views.autor_update, name="autor_update"),
    path("autores/delete/<pk>", views.autor_delete, name="autor_delete"),
    # Plantilla de Detalle
    path("autor/<pk>", views.AutorDetailView.as_view(), name="autor"),
    # Ejemplares
    path("ejemplares/", views.EjemplarListView.as_view(), name="ejemplares"),
    # path("ejemplares/", views.ejemplar_list, name="ejemplares"),
    path("ejemplares/new/", views.ejemplar_new, name="ejemplar_new"),
    path("ejemplares/update/<pk>", views.ejemplar_update, name="ejemplar_update"),
    path("ejemplares/delete/<pk>", views.ejemplar_delete, name="ejemplar_delete"),
    # Idiomas
    # path("idiomas/", views.idioma_list, name="idiomas"),
    path("idiomas/", views.IdiomaListView.as_view(), name="idiomas"),
    path("idiomas/new/", views.idioma_new, name="idioma_new"),
    path("idiomas/update/<pk>", views.idioma_update, name="idioma_update"),
    path("idiomas/delete/<pk>", views.idioma_delete, name="idioma_delete"),
]
