from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    password1= forms.CharField(label="Ingrese Contraseña",widget=forms.PasswordInput)
    password1= forms.CharField(label="Repetir Contraseña",widget=forms.PasswordInput)
    
    class Meta:
        model= User
        fields = ["username","email","password1","password2"]
        textos_ayuda = {k: "" for k in fields}