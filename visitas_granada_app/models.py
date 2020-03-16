from django.db import models

class Visita(models.Model):
	nombre      = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=1000)
	likes       = models.IntegerField(default=0)
	fecha_pub = models.DateTimeField('Fecha de publicación', auto_now_add=True)
	foto = models.ImageField(default='fotos/default.png')

class Comentario(models.Model):
	visita      = models.ForeignKey(Visita, on_delete=models.CASCADE, related_name='comentarios')
	texto       = models.CharField(max_length=500)