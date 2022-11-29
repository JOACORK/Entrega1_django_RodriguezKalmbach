from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from PersonajesApp.forms import CrearPersonaje
from PersonajesApp.models import *
# Create your views here.


def inicio(request):
    return render(request, 'inicio.html')

def creacion(request):
    if request.method == "POST":
        creacion = CrearPersonaje(request.POST)
        if creacion.is_valid():
            informacion = creacion.cleaned_data
            # Para Clase Personaje
            nombre=informacion["nombre"]
            raza= informacion["raza"][0]
            edad = informacion["edad"]
            altura = informacion["altura"]
            peso = informacion["peso"]
            # Para Clase Profesion
            profesion = informacion["profesion"][0]
            expertis = informacion["expertis"][0]
            renombre = informacion["renombre"][0]
            # Para Clase Familia
            familia = informacion["familia"]
            antiguedad = informacion["antiguedad"]
            profesionFamilia = informacion["profesionFamilia"][0]
            
            personaje = DatosPersonaje(nombre=nombre,raza= raza, edad = edad,  altura = altura,peso = peso) 
            personaje.save()
            
            profesion = DatosProfesion(profesion=profesion,expertis=expertis,renombre=renombre)
            profesion.save()
            
            profesionFamiliar = DatosFamilia(familia=familia,antiguedad=antiguedad,profesionFamilia=profesionFamilia)
            profesionFamiliar.save()
            
            return render(request,"inicio.html",{"mensaje" : "Personaje Creado!"})
    
    else:
        creacion = CrearPersonaje()
        
    return render(request, 'creacion.html', {"creacion":creacion})


