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
    # Urls para la API REST
    path('api/visitas/', csrf_exempt(VisitaListadoAPI.as_view()), name='listado_api'), 
    path('api/visitas/<int:visita_id>/', csrf_exempt(VisitaDetalleAPI.as_view()), name='detalle_api'),
    path('api/visitas/likes/<int:visita_id>/', csrf_exempt(VisitaLikesAPI.as_view()), name='likes_api'),
    path('api/visitas/comentarios/<int:visita_id>/', csrf_exempt(VisitaComentariosAPI.as_view()), name='comentarios_api'),
    path('api/token/', csrf_exempt(GetJWT.as_view()), name='token_api'),
]