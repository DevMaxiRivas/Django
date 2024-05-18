# Para ver la imagen en el administrador uso format_html
from django.utils.html import format_html

from django.contrib import admin

# Register your models here.
from catalogo.models import Autor, Genero, Idioma, Libro, Ejemplar

admin.site.register(Genero)
admin.site.register(Idioma)  # dejar esta línea como está ;)


# Define la clase Admin
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "isbn", "muestra_genero", "muestra_portada")

    # Representación HTML de la imagen
    def muestra_portada(self, obj):
        if obj.portada:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.portada.url,
            )
        return "No Image"

    muestra_portada.short_description = "Portada"


class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "fechaNac", "fechaDeceso", "muestra_retrato")

    # Representación HTML de la imagen
    def muestra_retrato(self, obj):
        if obj.retrato:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.retrato.url,
            )
        return "No Image"

    muestra_retrato.short_description = "Retrato"


class EjemplarAdmin(admin.ModelAdmin):
    list_display = ("libro", "estado", "fechaDevolucion")


# Registra clase Admin junto al modelo base
admin.site.register(Ejemplar, EjemplarAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
