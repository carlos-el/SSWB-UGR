from django.urls import path

from . import views

urlpatterns = [
    # ex: /visitas/
    path('', views.listado, name='listado'),
    path('visitas/', views.listado, name='listado'),
    path('visitas/<int:visita_id>/', views.detalle, name='detalle'),
]