from django_web_project.settings import BASE_DIR, STATIC_URL
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Visita, Comentario
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.contrib import messages

# Create your views here.



class VisitaListado(View):
    def get(self, request):
        ultimas_visitas = Visita.objects.order_by('-fecha_pub')[:10]
        context = {'visitas': ultimas_visitas}
        return render(request, 'listado.html', context)


class VisitaDetalle(View):
    def get(self, request, visita_id):
        visita = get_object_or_404(Visita, pk=visita_id)

        editForm = VisitaForm(initial={'nombre': visita.nombre, 'descripcion': visita.descripcion})

        context = {'visita': visita, 'form': editForm, 'errors': []}
        return render(request, 'detalle.html', context)

    # En realidad es un PUT camuflado pro que HTML no permite enviar PUT en formularios
    def post(self, request, visita_id):
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

    # def delete(self):
    #     pass


class VisitaNueva(View):
    def get(self, request):
        # Si no se es staff no se puede añadir visitas
        if not request.user.is_staff:
            raise PermissionDenied

        form = VisitaForm()

        context = {'form': form}
        return render(request, 'nueva_visita.html', context)

    def post(self, request):
        # Si no se es staff no se puede añadir visitas
        if not request.user.is_staff:
            raise PermissionDenied

        form = VisitaForm(request.POST, request.FILES)

        if form.is_valid():
            form.create()
            messages.success(request, "Visita creada con éxito.")

            return redirect('/')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)

        context = {'form': form}
        return render(request, 'nueva_visita.html', context)

class VisitaBorrar(View):
    def get(self, request, visita_id):
        # Si no se es staff no se puede añadir visitas
        if not request.user.is_staff:
            raise PermissionDenied

        visita = get_object_or_404(Visita, pk=visita_id)

        visita.delete()
        messages.success(request, "Visita eliminada con éxito.")

        return redirect('/')

        
class Login(View):
    def get(self, request):
        message = []
        next = request.GET.get('next', '')
        if(next):
            message.append("Debes iniciar sesión para acceder al contenido")

        form = UserLogInForm(initial={'next': next})
        return render(request, "login.html", {'form': form, 'errors': message})

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
    def get(self, request):
        logout(request)
        return redirect('/')