from django_web_project.settings import BASE_DIR, STATIC_URL
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Visita, Comentario

# Create your views here.

def listado(request):
    ultimas_visitas = Visita.objects.order_by('-fecha_pub')[:10]
    print(ultimas_visitas.first().comentarios.all())
    context = {'visitas': ultimas_visitas}
    return render(request, 'listado.html', context)

def detalle(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)

    context = {'visita': visita}
    return render(request, 'detalle.html', context)