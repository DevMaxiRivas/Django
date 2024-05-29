# Desarrollo de Home
from django.shortcuts import render
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor

# Vista Basada en clases
from django.views import generic

# Vista de detalle basada en Clases
from django.http import Http404

# Formularios
from django.shortcuts import redirect, get_object_or_404
from catalogo.forms import GeneroForm, AutorForm


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


# Formularios
# Generos
def genero_new(request):
    if request.method == "POST":
        formulario = GeneroForm(request.POST)

        if formulario.is_valid():
            genero = formulario.save(commit=False)
            genero.nombre = formulario.cleaned_data["nombre"]
            genero.save()
            return redirect("generos")

    else:
        formulario = GeneroForm()

    return render(request, "genero_new.html", {"formulario": formulario})


def genero_update(request, pk):
    genero = get_object_or_404(Genero, pk=pk)

    if request.method == "POST":
        formulario = GeneroForm(request.POST, instance=genero)
        if formulario.is_valid():
            genero = formulario.save(commit=False)
            genero.nombre = formulario.cleaned_data["nombre"]
            genero.save()
            return redirect("generos")
    else:
        formulario = GeneroForm(instance=genero)

    return render(request, "genero_new.html", {"formulario": formulario})


def genero_list(request):
    # Obtener todos los géneros de la base de datos
    generos = Genero.objects.all()
    # Crear un contexto con los géneros obtenidos
    context = {
        "generos": generos,
    }
    # Renderizar la plantilla con el contexto
    return render(request, "genero_list.html", context)


# Autores
def autor_new(request):
    if request.method == "POST":
        formulario = AutorForm(request.POST)

        if formulario.is_valid():
            autor = formulario.save(commit=False)
            autor.nombre = formulario.cleaned_data["nombre"]
            autor.apellido = formulario.cleaned_data["apellido"]
            autor.fechaNac = formulario.cleaned_data["fechaNac"]
            autor.fechaDeceso = formulario.cleaned_data["fechaDeceso"]
            autor.retrato = formulario.cleaned_data["retrato"]
            autor.save()
            return redirect("autores2")

    else:
        formulario = AutorForm()

    return render(request, "autor_new.html", {"formulario": formulario})


def autor_update(request, pk):
    autor = get_object_or_404(Autor, pk=pk)

    if request.method == "POST":
        formulario = AutorForm(request.POST, instance=autor)
        if formulario.is_valid():
            autor = formulario.save(commit=False)
            autor.nombre = formulario.cleaned_data["nombre"]
            autor.apellido = formulario.cleaned_data["apellido"]
            autor.fechaNac = formulario.cleaned_data["fechaNac"]
            autor.fechaDeceso = formulario.cleaned_data["fechaDeceso"]
            autor.save()
            return redirect("autores")
    else:
        formulario = AutorForm(instance=autor)

    return render(request, "autor_new.html", {"formulario": formulario})


def autor_list(request):
    # Obtener todos los géneros de la base de datos
    autores = Autor.objects.all()
    # Crear un contexto con los géneros obtenidos
    context = {
        "autores": autores,
    }
    # Renderizar la plantilla con el contexto
    return render(request, "autores_list.html", context)
