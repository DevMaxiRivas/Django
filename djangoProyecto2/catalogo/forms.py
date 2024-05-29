from django import forms
from catalogo.models import Genero, Autor


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
