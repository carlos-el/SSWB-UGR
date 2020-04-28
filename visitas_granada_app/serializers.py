
from .models import Visita
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
        )

