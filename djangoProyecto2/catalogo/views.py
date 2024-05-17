from django.shortcuts import render
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor


def index(request):
    nroGeneros = Genero.objects.all().count()
    nroIdiomas = Idioma.objects.all().count()

    nroLibros = Libro.objects.all().count()
    nroEjemplares = Ejemplar.objects.all().count()
    nroDisponibles = Ejemplar.objects.filter(estado__exact="d").count()
    nroAutores = Autor.objects.count()  # El 'all()' esta implícito por defecto.
    context = {
        "nroGeneros": nroGeneros,
        "nroIdiomas": nroIdiomas,
        "nroLibros": nroLibros,
        "nroEjemplares": nroEjemplares,
        "nroDisponibles": nroDisponibles,
        "nroAutores": nroAutores,
    }

    return render(request, "index.html", context)
