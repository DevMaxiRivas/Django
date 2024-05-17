from django.contrib import admin

# Register your models here.
from catalogo.models import Autor, Genero, Idioma, Libro, Ejemplar

admin.site.register(Genero)
admin.site.register(Idioma)  # dejar esta línea como está ;)


# Define la clase Admin
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "isbn", "muestra_genero")


class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "fechaNac", "fechaDeceso")


class EjemplarAdmin(admin.ModelAdmin):
    list_display = ("libro", "estado", "fechaDevolucion")


# Registra clase Admin junto al modelo base
admin.site.register(Ejemplar, EjemplarAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
