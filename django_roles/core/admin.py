from django.contrib import admin

from .models import (
    Course,
    LugaresDeEvento,
    Localidades,
    Provincias,
    Eventos,
    Ventas,
    Registration,
    Mark,
    Attendance,
)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "class_quantity", "teacher")
    list_filter = ("teacher",)


admin.site.register(Course, CourseAdmin)


class LugaresDeEventoAdmin(admin.ModelAdmin):
    list_display = (
        "id_le",
        "desc_le",
        "lat_le",
        "lng_le",
    )


admin.site.register(LugaresDeEvento, LugaresDeEventoAdmin)
admin.site.register(Localidades)
admin.site.register(Provincias)
admin.site.register(Eventos)


class VentasAdmin(admin.ModelAdmin):
    readonly_fields = ["pr_ve"]


admin.site.register(Ventas, VentasAdmin)

# Cursos
admin.site.register(Registration)
admin.site.register(Mark)
admin.site.register(Attendance)
