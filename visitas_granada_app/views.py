from django_web_project.settings import BASE_DIR, STATIC_URL
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Visita, Comentario, Perfil
from .serializers import VisitaSerializer, ComentarioSerializer
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from functools import wraps

import jwt, json
from django_web_project import settings
from datetime import datetime, timedelta
import string
import random

# DECORATORS
# TODO Mover decorators a otro fichero (junto con su import de wraps)
# Decorador que comprueba que la petición contiene un token JWT y que es válido
def check_request_jwt_decorator(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', None)
            if token is None:
                return JsonResponse({'error': 'Token de autenticacion no encontrado'}, status=401)
            # Obtenemos la parte que contiene el token
            token = token.split("Bearer ")[1]
            jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            perfil = Perfil.objects.get(token = token)
            request.user = perfil.user
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expirado'}, status=401)
        except:
            return JsonResponse({'error': 'Token incorrecto o mal especificado'}, status=401)

        return fn(request, *args, **kwargs)
    return wrapper

####################################
# Views para la página web 
####################################

class VisitaListado(View):
    # Controlador para mostrar todas las visitas desde la web
    def get(self, request):
        # TODO Añadir paginación
        ultimas_visitas = Visita.objects.order_by('-fecha_pub')[:10]
        context = {'visitas': ultimas_visitas}
        return render(request, 'listado.html', context)

class VisitaDetalle(View):
    # Controlador para mostrar una visita concreta desde la web
    def get(self, request, visita_id):
        visita = get_object_or_404(Visita, pk=visita_id)
        editForm = VisitaForm(initial={'nombre': visita.nombre, 'descripcion': visita.descripcion, 'lat': visita.lat, 'lon':visita.lon})
        context = {'visita': visita, 'form': editForm, 'errors': []}
        return render(request, 'detalle.html', context)

    # Controlador para editar una visita concreta desde la web
    def post(self, request, visita_id):
        # En realidad es un PUT camuflado por que HTML no permite enviar PUT en formularios

        # Si no se es staff no se puede editar
        if not request.user.is_staff:
            raise PermissionDenied

        visita = get_object_or_404(Visita, pk=visita_id)        
        form = VisitaForm(request.POST, request.FILES)

        if form.is_valid():
            visita = form.save(visita)
            messages.success(request, "Visita modificada con éxito")
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)

        context = {'visita': visita, 'form': form}
        return render(request, 'detalle.html', context)

class VisitaNueva(View):
    # Controlador para obtener el formulario para crear una visita
    def get(self, request):
        # Si no se es staff no se puede añadir visitas
        if not request.user.is_staff:
            raise PermissionDenied

        form = VisitaForm()

        context = {'form': form}
        return render(request, 'nueva_visita.html', context)

    # Procesa el formulario de creacion de visita de la página web
    def post(self, request):
        # Si no se es staff no se puede añadir visitas
        if not request.user.is_staff:
            raise PermissionDenied

        form = VisitaForm(request.POST, request.FILES)

        if form.is_valid():
            form.create()
            messages.success(request, "Visita creada con éxito")

            return redirect('/')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)

        context = {'form': form}
        return render(request, 'nueva_visita.html', context)

class VisitaBorrar(View):
    # Controlador para eliminar una visita desde la web
    def get(self, request, visita_id):
        # Si no se es staff no se puede añadir visitas
        if not request.user.is_staff:
            raise PermissionDenied

        visita = get_object_or_404(Visita, pk=visita_id)

        # Si la foto de la visita no es la default la borramos 
        if visita.foto.name != 'fotos/default.png':
            visita.foto.delete(save=False)

        visita.delete()
        
        messages.success(request, "Visita eliminada con éxito")

        return redirect('/')
   
class Login(View):
    # Controlador para obtener el formulario de login desde la web
    def get(self, request):
        message = []
        next = request.GET.get('next', '')
        if(next):
            message.append("Debes iniciar sesión para acceder al contenido")

        form = UserLogInForm(initial={'next': next})
        return render(request, "login.html", {'form': form, 'errors': message})

    # Controlador para procesar los datos del login desde la web
    def post(self, request):
        # Obtener datos del POST
        form = UserLogInForm(request.POST)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Loguear al usuario
            login(request, user)
            
            # Redirigir siempre despues de un POST existoso
            # Comprobar si habia redirección pendiente.
            next = request.POST.get('next', '')
            if(next):
                return redirect(next)

            return redirect('/')
        else:
            message = ["Nombre de usuario o contraseña incorrectos"]
            form = UserLogInForm()  # Enviar nuevo formulario vacio
            return render(request, "login.html", {'form': form, 'errors': message})

class Logout(View):
    # Controlador que desloguea a un usuario logueado desde la web
    def get(self, request):
        logout(request)
        return redirect('/')


####################################
# API REST Views
####################################

class VisitaListadoAPI(View):
    def get(self, request):
        visitas_json = []
        visitas = Visita.objects.order_by('-fecha_pub')
        visitas_json = VisitaSerializer(instance=visitas, many=True).data
        return JsonResponse({'visitas': visitas_json})

    @method_decorator(check_request_jwt_decorator)
    def post(self, request):
        # Si no es staff no se puede realizar la accion
        if not request.user.is_staff:
            return JsonResponse({'error': 'Permiso denegado, no puede realizar esta accion'}, status=403)

        # Comprobar que los datos son validos y guardar la visita
        form = VisitaForm(request.POST, request.FILES)
        if form.is_valid():
            visita = form.create()
            visita_json = VisitaSerializer(instance=visita).data
            return JsonResponse(visita_json, status=201)
        else:
            errors = []
            for field in form.errors:
                for error in form.errors[field]:
                    errors.append(error)    
            return JsonResponse({'error': errors}, status=400)

class VisitaDetalleAPI(View):
    def get(self, request, visita_id):
        try:
            visita = Visita.objects.get(pk = visita_id)
        except Visita.DoesNotExist:
            return JsonResponse({'error': 'Visita no encontrada'}, status=404)

        visita_json = VisitaSerializer(instance=visita).data
        return JsonResponse(visita_json)

    @method_decorator(check_request_jwt_decorator)
    def put(self, request, visita_id):
        # Si no es staff no se puede realizar la accion
        if not request.user.is_staff:
            return JsonResponse({'error': 'Permiso denegado, no puede realizar esta accion'}, status=403)

        # Comprobamos que la visita existe
        try:
            visita = Visita.objects.get(pk = visita_id)
        except Visita.DoesNotExist:
            return JsonResponse({'error': 'Visita no encontrada'}, status=404)

        # Comprobar que los datos son validos y guardar la visita
        form = VisitaForm(request.PUT, request.FILES)
        if form.is_valid():
            visita = form.save(visita)
            visita_json = VisitaSerializer(instance=visita).data
            return JsonResponse(visita_json, status=200)
        else:
            errors = []
            for field in form.errors:
                for error in form.errors[field]:
                   errors.append(error)    
            return JsonResponse({'error': errors}, status=400)

    @method_decorator(check_request_jwt_decorator)
    def delete(self, request, visita_id):
        # Si no es staff no se puede realizar la accion
        if not request.user.is_staff:
            return JsonResponse({'error': 'Permiso denegado, no puede realizar esta accion'}, status=403)

        # Comprobamos que la visita existe
        try:
            visita = Visita.objects.get(pk = visita_id)
        except Visita.DoesNotExist:
            return JsonResponse({'error': 'Visita no encontrada'}, status=404)

        visita.delete()
        return JsonResponse({'message': 'Visita eliminada con exito'}, status=200)

class VisitaLikesAPI(View):
    def get(self, request, visita_id):
        try:
            visita = Visita.objects.get(pk = visita_id)
        except Visita.DoesNotExist:
            return JsonResponse({'error': 'Visita no encontrada'}, status=404)

        return JsonResponse({'likes': visita.likes})
 
    # TODO manejar la concurrencia 
    # TODO Permitir que solo se vote una vez a ser posible
    def put(self, request, visita_id):
        try:
            visita = Visita.objects.get(pk = visita_id)
        except Visita.DoesNotExist:
            return JsonResponse({'error': 'Visita no encontrada'}, status=404)

        likes = request.PUT.get('likes', None)
        
        if likes is None:
            return JsonResponse({'error': 'Valor de likes no provisto'}, status=400)

        try:
            likes = int(likes)
        except:
            return JsonResponse({'error': 'Valor de likes erroneo'}, status=400)

        if likes == visita.likes + 1 or likes == visita.likes - 1:
            visita.likes = likes
            visita.save()
            return JsonResponse({'likes': visita.likes}, status=200)
        else:
            return JsonResponse({'error': 'Valor de likes no permitido'}, status=400)


class VisitaComentariosAPI(View):
    def get(self, request, visita_id):
        try:
            visita = Visita.objects.get(pk = visita_id)
        except Visita.DoesNotExist:
            return JsonResponse({'error': 'Visita no encontrada'}, status=404)

        comentarios_json = ComentarioSerializer(instance=visita.comentarios, many=True).data
        return JsonResponse({'comentarios': comentarios_json})

    # def post(self, request, visita_id):
    #     pass


class GetJWT(View):
    def post(self, request):
        # Comprobamos que el usuario existe
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        # Si existe devolvemos el token y se lo asignamos en la base de datos
        if user is not None:
            # Si existe devolvemos el token y se lo asignamos en la base de datos
            # La carga del token creado contiene un string aleatorio de 10 caracteres, la fecha de creacion y la de expiracion
            date = datetime.now()
            rand_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            token = jwt.encode({'random_component': rand_str,'created': date.strftime("%m_%d_%Y-%H_%M_%S"), 'exp': date + timedelta(seconds = 3600)}, settings.SECRET_KEY, algorithm='HS256').decode("utf-8") 
            user.perfil.token = token
            user.perfil.save()
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'error': 'Credenciales incorrectas'}, status=400)

        

# TODO hacer decorator para comprobar isStaff? tendria que llamarse despues de check_jwt  ya que es el q establece request.user
