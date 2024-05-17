from django.contrib import admin

# Register your models here.
from catalogo.models import Autor, Genero, Idioma, Libro, Ejemplar

admin.site.register(Autor)
admin.site.register(Genero)
admin.site.register(Idioma)  # dejar esta línea como está ;)
admin.site.register(Libro)
admin.site.register(Ejemplar)
