# Desarrollo de Home
from django.shortcuts import render
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor

# Vista Basada en clases
from django.views import generic

# Vista de detalle basada en Clases
from django.http import Http404

# Formularios
from django.shortcuts import redirect, get_object_or_404
from catalogo.forms import GeneroForm, AutorForm, EjemplarForm, IdiomaForm, LibroForm

# Carousel dinámico

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from catalogo.serializers import dataSerializer


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


class EjemplarListView(generic.ListView):
    model = Ejemplar
    paginate_by = 6

    context_object_name = "ejemplares"
    # en este caso va un modelo
    queryset = Ejemplar.objects.all()
    # si quiero filtrar
    template_name = "ejemplares.html"
    # nombre del template


class GeneroListView(generic.ListView):
    model = Genero
    # paginate_by = 2

    context_object_name = "generos"
    # en este caso va un modelo
    queryset = Genero.objects.all()
    # si quiero filtrar
    template_name = "generos.html"
    # nombre del template


class IdiomaListView(generic.ListView):
    model = Idioma
    # paginate_by = 2

    context_object_name = "idiomas"
    # en este caso va un modelo
    queryset = Idioma.objects.all()
    # si quiero filtrar
    template_name = "idiomas.html"
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

    return render(request, "element_new.html", {"formulario": formulario})


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

    return render(request, "element_new.html", {"formulario": formulario})


def genero_delete(request, pk):
    genero = get_object_or_404(Genero, pk=pk)

    genero.delete()

    return redirect("generos")


# def genero_list(request):
#     # Obtener todos los géneros de la base de datos
#     generos = Genero.objects.all()
#     # Crear un contexto con los géneros obtenidos
#     context = {
#         "generos": generos,
#     }
#     # Renderizar la plantilla con el contexto
#     return render(request, "genero_list.html", context)


# Libros
def libro_new(request):
    if request.method == "POST":
        formulario = LibroForm(request.POST, request.FILES)

        if formulario.is_valid():
            libro = formulario.save(commit=False)
            libro.titulo = formulario.cleaned_data["titulo"]
            libro.autor = formulario.cleaned_data["autor"]
            libro.resumen = formulario.cleaned_data["resumen"]
            libro.isbn = formulario.cleaned_data["isbn"]
            libro.portada = formulario.cleaned_data["portada"]
            libro.save()
            # TENER EN CUENTA PARA RELACIONES ManyToManyField
            formulario.save_m2m()
            return redirect("libros")

    else:
        formulario = LibroForm()

    return render(request, "element_new.html", {"formulario": formulario})


def libro_update(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        formulario = LibroForm(request.POST, request.FILES, instance=libro)
        if formulario.is_valid():
            libro = formulario.save(commit=False)
            libro.titulo = formulario.cleaned_data["titulo"]
            libro.autor = formulario.cleaned_data["autor"]
            libro.resumen = formulario.cleaned_data["resumen"]
            libro.isbn = formulario.cleaned_data["isbn"]
            libro.portada = formulario.cleaned_data["portada"]
            libro.save()
            # TENER EN CUENTA PARA RELACIONES ManyToManyField
            formulario.save_m2m()
            return redirect("libros")
    else:
        formulario = LibroForm(instance=libro)

    return render(request, "element_new.html", {"formulario": formulario})


def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    libro.delete()

    return redirect("libros")


# Autores
def autor_new(request):
    if request.method == "POST":
        formulario = AutorForm(request.POST, request.FILES)

        if formulario.is_valid():
            autor = formulario.save(commit=False)
            autor.nombre = formulario.cleaned_data["nombre"]
            autor.apellido = formulario.cleaned_data["apellido"]
            autor.fechaNac = formulario.cleaned_data["fechaNac"]
            autor.fechaDeceso = formulario.cleaned_data["fechaDeceso"]
            autor.retrato = formulario.cleaned_data["retrato"]
            autor.save()
            return redirect("autores")

    else:
        formulario = AutorForm()

    return render(request, "element_new.html", {"formulario": formulario})


def autor_update(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == "POST":
        formulario = AutorForm(request.POST, request.FILES, instance=autor)
        if formulario.is_valid():
            autor.apellido = formulario.cleaned_data["apellido"]
            autor.nombre = formulario.cleaned_data["nombre"]
            autor.fechaNac = formulario.cleaned_data["fechaNac"]
            autor.fechaDeceso = formulario.cleaned_data["fechaDeceso"]
            autor.retrato = formulario.cleaned_data["retrato"]
            autor.save()
            return redirect("autores")
        else:
            # redirijo
            return render(request, "element_new.html", {"formulario": formulario})
    else:
        formulario = AutorForm(instance=autor)

    return render(request, "element_new.html", {"formulario": formulario})


def autor_delete(request, pk):
    autor = get_object_or_404(Autor, pk=pk)

    autor.delete()

    return redirect("autores")


# Ejemplares
def ejemplar_new(request):
    if request.method == "POST":
        formulario = EjemplarForm(request.POST)

        if formulario.is_valid():
            ejemplar = formulario.save(commit=False)
            ejemplar.id = formulario.cleaned_data["id"]
            ejemplar.libro = formulario.cleaned_data["libro"]
            ejemplar.estado = formulario.cleaned_data["estado"]
            ejemplar.fechaDevolucion = formulario.cleaned_data["fechaDevolucion"]
            ejemplar.save()
            return redirect("ejemplares")

    else:
        formulario = EjemplarForm()

    return render(request, "element_new.html", {"formulario": formulario})


def ejemplar_update(request, pk):
    ejemplar = get_object_or_404(Ejemplar, pk=pk)

    if request.method == "POST":
        formulario = EjemplarForm(request.POST, instance=ejemplar)

        if formulario.is_valid():
            ejemplar = formulario.save(commit=False)
            ejemplar.libro = formulario.cleaned_data["libro"]
            ejemplar.estado = formulario.cleaned_data["estado"]
            ejemplar.fechaDevolucion = formulario.cleaned_data["fechaDevolucion"]
            ejemplar.save()
            return redirect("ejemplares")

    else:
        formulario = EjemplarForm(instance=ejemplar)

    return render(request, "element_new.html", {"formulario": formulario})


def ejemplar_delete(request, pk):
    ejemplar = get_object_or_404(Ejemplar, pk=pk)

    ejemplar.delete()

    return redirect("ejemplares")


# def ejemplar_list(request):
#     # Obtener todos los géneros de la base de datos
#     ejemplares = Ejemplar.objects.all()
#     # Crear un contexto con los géneros obtenidos
#     context = {
#         "ejemplares": ejemplares,
#     }
#     # Renderizar la plantilla con el contexto
#     return render(request, "ejemplar_list.html", context)


# Idiomas
def idioma_new(request):
    if request.method == "POST":
        formulario = IdiomaForm(request.POST)

        if formulario.is_valid():
            idioma = formulario.save(commit=False)
            idioma.nombre = formulario.cleaned_data["nombre"]
            idioma.save()
            return redirect("idiomas")

    else:
        formulario = IdiomaForm()

    return render(request, "element_new.html", {"formulario": formulario})


def idioma_update(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk)

    if request.method == "POST":
        formulario = IdiomaForm(request.POST, instance=idioma)

        if formulario.is_valid():
            idioma = formulario.save(commit=False)
            idioma.nombre = formulario.cleaned_data["nombre"]
            idioma.save()
            return redirect("idiomas")

    else:
        formulario = IdiomaForm(instance=idioma)

    return render(request, "element_new.html", {"formulario": formulario})


# Manejo de Ventanas Modales
# def idioma_list(request):
#     idiomas = Idioma.objects.all()
#     context = {"idiomas": idiomas}
#     return render(request, "idioma_list.html", context)


def idioma_delete(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk)

    idioma.delete()

    return redirect("idiomas")


# Carousel dinámico
def index_carousel(request):
    return render(request, "index2.html")


class carousel_items(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = dataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
