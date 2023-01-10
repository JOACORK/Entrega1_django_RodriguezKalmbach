from  django import forms
from  AppRegistro.forms import RegistroUsuarioForm
from django.contrib.auth.models import User

class EdicionUsuarioForm(RegistroUsuarioForm):

    # Obligatorios
    email = forms.EmailField(label="Ingrese su email:")
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="Imagen")
