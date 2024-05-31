from django import forms
from catalogo.models import Genero, Autor, Ejemplar
from django.forms.widgets import NumberInput


class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ("nombre",)


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


ESTADO_EJEMPLAR = (
    ("m", "en Mantenimiento"),
    ("p", "Prestado"),
    ("d", "Disponible"),
    ("r", "Reservado"),
)


class EjemplarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id"].disabled = True

    estado = forms.ChoiceField(
        widget=forms.Select, choices=ESTADO_EJEMPLAR, initial="d"
    )

    class Meta:
        model = Ejemplar
        fields = ("id", "libro", "estado")
