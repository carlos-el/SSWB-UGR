from django.db import models
from django.contrib.auth.models import User


class Visita(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    fecha_pub = models.DateTimeField('Fecha de publicación', auto_now_add=True)
    foto = models.ImageField(default='fotos/default.png', upload_to="fotos/")
    lat = models.FloatField(default=37.196459)
    lon = models.FloatField(default=-3.6261883)


class Comentario(models.Model):
    visita = models.ForeignKey(
        Visita, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.CharField(max_length=500)
    # Fecha
    # Usuario


# Este modelo permite añadir características al usuario por defecto de Django pero
# sin tener que tocar nada sobre este.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=512)
