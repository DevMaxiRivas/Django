from rest_framework import serializers  # type: ignore
from catalogo.models import Autor


class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ["id", "nombre", "apellido", "retrato"]
