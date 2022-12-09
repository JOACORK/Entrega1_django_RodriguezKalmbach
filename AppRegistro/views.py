from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
#from django.http import HttpResponse
from AppRegistro.forms import RegistroUsuarioForm
#from AppRegistro.models import *
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            form.save()
            #TODO Logear automáticamente con el usuario creado con autenticate y login
            
            return render(request,"PersonajesApp/inicio.html",{"mensaje":f"Usuario {username} creado correctamente!"})
        else:
            return render(request,"AppRegistro/nuevoUsuario.html",{"form":form,"mensaje":"Error al crear el Usuario"})
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'nuevoUsuario.html',{"form":form})