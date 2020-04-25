from django.urls import path
from visitas_granada_app.views import *


urlpatterns = [
    # ex: /visitas/
    path('', VisitaListado.as_view(), name='listado'),
    path('visitas/', VisitaListado.as_view(), name='listado'),
    path('visitas/<int:visita_id>/', VisitaDetalle.as_view(), name='detalle'),
    path('visita_nueva/', VisitaNueva.as_view(), name='nueva'),
    path('visita_borrar/<int:visita_id>/', VisitaBorrar.as_view(), name='borrar'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]