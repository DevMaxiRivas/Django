from django.contrib import admin

# Register your models here.
from catalogo.models import Autor, Libro, Genero, Ejemplar, Idioma


class LibroAdmin(admin.ModelAdmin):
    pass


class AutorAdmin(admin.ModelAdmin):
    pass


class GeneroAdmin(admin.ModelAdmin):
    pass


class EjemplarAdmin(admin.ModelAdmin):
    pass


class IdiomaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Libro, LibroAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Ejemplar, EjemplarAdmin)
admin.site.register(Idioma, IdiomaAdmin)
