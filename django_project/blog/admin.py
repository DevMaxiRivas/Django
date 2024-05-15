from django.contrib import admin

# Register your models here.
from blog.models import Posteo, Categoria

class PosteoAdmin(admin.ModelAdmin):
    pass

class CategoriaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Posteo, PosteoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
