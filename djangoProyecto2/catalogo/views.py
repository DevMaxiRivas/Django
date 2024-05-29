# Desarrollo de Home
from django.shortcuts import render
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor

# Vista Basada en clases
from django.views import generic

# Vista de detalle basada en Clases
from django.http import Http404


# Desarrollo de Home
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


# Vista Basada en clases
class LibroListView(generic.ListView):
    model = Libro
    paginate_by = 2

    context_object_name = "libros"
    # en este caso va un modelo
    queryset = Libro.objects.all()
    # si quiero filtrar
    template_name = "libros.html"
    # nombre del template


# En el caso de arriba, sólo se envía libros (un listado). Si se quiere renderizar más datos, se puede implementar
# la función get_context_data()

# class LibroListView(generic.ListView):
#     model = Libro
#     template_name='libros.html'
#     # nombre del template
#     def get_context_data(self, **kwargs):
#     libros = Libro.objects.all()
#     context = super(LibroListView, self).get_context_data(**kwargs)

#     context['libros'] = libros


#     return context


class AutorListView(generic.ListView):
    model = Autor
    paginate_by = 2

    context_object_name = "autores"
    # en este caso va un modelo
    queryset = Autor.objects.all()
    # si quiero filtrar
    template_name = "autores.html"
    # nombre del template


# Vista de detalle basada en Clases
class LibroDetailView(generic.DetailView):
    model = Libro
    template_name = "libro.html"

    # es obligatorio el nombre del template
    def libro_detail_view(request, pk):
        try:
            libro = Libro.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Oops! El Libro no existe")
        context = {
            "libro": libro,
        }

        return render(request, "libro.html", context)


class AutorDetailView(generic.DetailView):
    model = Autor
    template_name = "autor.html"

    # es obligatorio el nombre del template
    def libro_detail_view(request, pk):
        try:
            autor = Autor.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Oops! El Libro no existe")
        context = {
            "autor": autor,
        }

        return render(request, "autor.html", context)


# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import generic
# from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor
# from catalogo.forms import GeneroForm, AutorForm


# # ....
# def genero_new(request):
#     if request.method == "POST":
#         formulario = GeneroForm(request.POST)

#     if formulario.is_valid():
#         genero = formulario.save(commit=False)
#         genero.nombre = formulario.cleaned_data["nombre"]
#         genero.save()
#         return redirect("generos")

#     else:
#         formulario = GeneroForm()
#         return render(request, "genero_new.html", {"formulario": formulario})
