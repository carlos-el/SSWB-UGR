# Fichero que al ser ejecutado poblará la base de datos de la app de Django con algunas visitas

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_web_project.settings')

import django
django.setup()

from visitas_granada_app.models import Visita, Comentario
	
if __name__ == "__main__":
		
	v = Visita.objects.create(nombre="Alhambra", descripcion="Texto Alhambra", likes=2)
	Comentario.objects.create(visita=v, texto="Buenas impresiones.")
	Comentario.objects.create(visita=v, texto="Me ha gustado.")

	v = Visita.objects.create(nombre="Corral del carbón", descripcion="Texto Corral del carbón", likes=4)
	Comentario.objects.create(visita=v, texto="Esta bien, un poco soso.")
	Comentario.objects.create(visita=v, texto="La fuente es bonita.")
	Comentario.objects.create(visita=v, texto="Los domingos hay mucha gente.")

	v = Visita.objects.create(nombre="Mirador de San Nicolás", descripcion="Texto Mirador de San Nicolás", likes=1)
	Comentario.objects.create(visita=v, texto="Un sitio agradable.")
	Comentario.objects.create(visita=v, texto="Bonitas vistas.")

	print(Visita.objects.all())