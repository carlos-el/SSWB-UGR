from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from visitas_granada_app.models import Visita


class UserLogInForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', min_length=4, max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={'placeholder': 'Contraseña'}))
    next = forms.CharField(initial='',  widget=forms.HiddenInput)
# TODO Al añadir el Register y al crear usuario hay que crear el perfil extendido con cada usuario que se cree


class VisitaForm(forms.Form):
    nombre = forms.CharField(label='Título', min_length=5, max_length=100, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            error_messages={'required': "El campo 'nombre' es obligatorio"})
    descripcion = forms.CharField(
                            label='Descripción', min_length=5, max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}),
                            required=True, error_messages={'required': "El campo 'descripcion' es obligatorio"})
    lat = forms.FloatField(label='Latitud', max_value=90,
                            min_value=-90, required=False,
                            error_messages={'max_value': "El valor de 'lat' debe estar entre 90 y -90",
                                           'min_value': "El valor de 'lat' debe estar entre 90 y -90",
                                           'invalid': "El campo 'lat' debe se un numero con hasta 6 decimales"})
    lon = forms.FloatField(label='Latitud', max_value=180,
                            min_value=-180, required=False,
                            error_messages={'max_value': "El valor de 'lon' debe estar entre 180 y -180",
                                           'min_value': "El valor de 'lon' debe estar entre 180 y -180",
                                           'invalid': "El campo 'lon' debe se un numero con hasta 6 decimales"})
    foto = forms.ImageField(required=False)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) < 5:
            self.add_error('nombre', "Título de la visita demasiado corto")
        if len(nombre) > 100:
            self.add_error('nombre', "Título de la visita demasiado largo")
        if not nombre[0].isupper():
            self.add_error(
                'nombre', "El título de la visita debe comenzar con mayúscula")
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) < 10:
            self.add_error(
                'descripcion', "Descripción de la visita demasiado corta")
        if len(descripcion) > 1000:
            self.add_error(
                'descripcion', "Descripción de la visita demasiado larga")
        if not descripcion[0].isupper():
            self.add_error(
                'descripcion', "La descripción de la visita debe comenzar con mayúscula")
        return descripcion

    # def clean_foto(self):
    #     pass

    # Método para actualizar una visita ya existente
    def save(self, visita):
        visita.nombre = self.cleaned_data['nombre']
        visita.descripcion = self.cleaned_data['descripcion']
        lat = self.cleaned_data['lat']
        lon = self.cleaned_data['lon']
        new_img = self.cleaned_data['foto']
        if lat is not None:
            visita.lat = lat
        if lon is not None:
            visita.lon = lon
        if new_img is not None:
            new_img.name = datetime.now().strftime("%m_%d_%Y-%H_%M_%S") + \
                '.' + new_img.image.format.lower()
            if visita.foto.name != 'fotos/default.png':
                print("valued in")
                visita.foto.delete(save=False)
            visita.foto = new_img

        visita.save()
        return visita

    # Método para crear una nueva visita
    def create(self):
        nombre = self.cleaned_data['nombre']
        descripcion = self.cleaned_data['descripcion']
        img = self.cleaned_data['foto']

        if img is not None:
            visita = Visita.objects.create(
                nombre=nombre, descripcion=descripcion, foto=img)
        else:
            visita = Visita.objects.create(
                nombre=nombre, descripcion=descripcion)

        return visita
