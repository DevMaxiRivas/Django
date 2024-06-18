from django.contrib import admin

from .models import *


class LugaresDeEventoAdmin(admin.ModelAdmin):
    list_display = (
        "id_le",
        "desc_le",
        "lat_le",
        "lng_le",
    )

class VentasAdmin(admin.ModelAdmin):
    readonly_fields = ["pr_ve"]


class BoletosAdmin(admin.ModelAdmin):
    readonly_fields = ["cli_bl", "evt_bl"]



admin.site.register(Provincias)
admin.site.register(Localidades)
admin.site.register(LugaresDeVenta)
admin.site.register(LugaresDeEvento, LugaresDeEventoAdmin)
admin.site.register(Secciones)
admin.site.register(Sectores)
admin.site.register(Asientos)
admin.site.register(Eventos)
admin.site.register(EventosPorSeccion)
admin.site.register(Ventas, VentasAdmin)
admin.site.register(Boletos, BoletosAdmin)


