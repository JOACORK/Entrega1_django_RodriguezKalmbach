from django.shortcuts import render

# Import para login, logout y register
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login, logout,authenticate

#from django.http import HttpResponse
from AppRegistro.forms import RegistroUsuarioForm

from django.contrib.auth.decorators import login_required

#from AppRegistro.models import *
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            #TODO Logear automáticamente con el usuario creado con autenticate y login
            
            return render(request,"inicio.html",{"mensaje":f"Usuario {username} creado correctamente!"})
        else:
            return render(request,"nuevoUsuario.html",{"form":form,"mensaje":"Error al crear el Usuario"})
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'nuevoUsuario.html',{"form":form})

# ----------- Login
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usu= form.cleaned_data.get("username")
            clave= form.cleaned_data.get("password")
            
            usuario = authenticate(username = usu, password= clave)
            
            if usuario is not None:
                login(request,usuario)
                return render(request, "inicio.html",{"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request, "login.html",{"mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request, "login.html",{"form":form,"mensaje":"Usuario o contraseña incorrectos"})
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{"form":form})