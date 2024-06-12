from django import forms
from catalogo.models import Genero, Autor, Ejemplar, Idioma, Libro
from django.forms.widgets import NumberInput


# Estructura de Formulario Genero
class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ("nombre",)


# Estructura de Formulario Libros
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = (
            "titulo",
            "autor",
            "resumen",
            "isbn",
            "genero",
            "portada",
        )


# Estructura de Formulario Autor
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = (
            "nombre",
            "apellido",
            "fechaNac",
            "fechaDeceso",
            "retrato",
        )

        widgets = {
            "fechaNac": NumberInput(attrs={"type": "date"}),
            "fechaDeceso": NumberInput(attrs={"type": "date"}),
        }

    def clean(self):
        super(AutorForm, self).clean()
        apellido = self.cleaned_data.get("apellido")
        nombre = self.cleaned_data.get("nombre")
        fechaNac = self.cleaned_data.get("fechaNac")
        fechaDeceso = self.cleaned_data.get("fechaDeceso")
        if len(apellido) < 3:
            self._errors["apellido"] = self.error_class(
                ["El apellido debe tener al menos 3 caracteres"]
            )
        if len(nombre) < 5:
            self._errors["nombre"] = self.error_class(
                ["El nombre debe tener al menos 5 caracteres"]
            )
        if fechaNac != None and fechaDeceso != None:
            if fechaDeceso < fechaNac:
                self._errors["fechaDeceso"] = self.error_class(
                    ["La fecha de deceso debe ser mayor a la de nacimiento"]
                )
        return self.cleaned_data


# Estructura de Formulario Ejemplares

ESTADO_EJEMPLAR = (
    ("m", "en Mantenimiento"),
    ("p", "Prestado"),
    ("d", "Disponible"),
    ("r", "Reservado"),
)


class EjemplarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esta linea cambia el id al crear un nuevo ejemplar
        # self.fields["id"].disabled = True

    estado = forms.ChoiceField(
        widget=forms.Select, choices=ESTADO_EJEMPLAR, initial="d"
    )

    class Meta:
        model = Ejemplar
        fields = ("id", "libro", "estado", "fechaDevolucion")
        widgets = {
            "fechaDevolucion": NumberInput(attrs={"type": "date"}),
        }


# Estructura de Formulario Idioma
class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ("nombre",)
