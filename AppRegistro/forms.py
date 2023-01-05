from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    password1= forms.CharField(label="Ingrese Contraseña",widget=forms.PasswordInput)
    password2= forms.CharField(label="Repetir Contraseña",widget=forms.PasswordInput)
    last_name = forms.CharField()
    first_name= forms.CharField()
    
    class Meta:
        model= User
        fields = ["username","email","password1","password2","last_name","first_name"]
        textos_ayuda = {k: "" for k in fields}
