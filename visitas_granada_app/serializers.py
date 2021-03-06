
from .models import Visita, Comentario
from rest_framework import serializers

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = (
            'id',
            'nombre',
            'descripcion',
            'likes',
            'fecha_pub',
            'foto',
            'lat',
            'lon'
        )

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = (
            'texto',
        )

