from django.shortcuts import render, redirect
from django.http import HttpResponse
from PersonajesApp.forms import CrearPersonaje, CrearFamilia, CrearPj
from PersonajesApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import time
# Funcionesútiles




# Create your views here.


def inicio(request):
    return render(request, 'inicio.html')

@login_required
def creacionPj(request):
    if request.method == "POST":
        creacion = CrearPj(request.POST)
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

            # guardar usuario
            #usuario = request.user
            #nombre_usuario = usuario.first_name

            #print(usuario)
            
            #time.sleep(10)

            # Crea personaje y profesion            
            personaje, creado = DatosPersonaje.objects.get_or_create(nombre=nombre,raza= raza, edad = edad,  altura = altura,peso = peso)

            profesion, creado = DatosProfesion.objects.get_or_create(profesion=profesion,expertis=expertis,renombre=renombre)

            # Crea tabla relacional entre personaje y profesion
            idPersonaje = personaje.idPersonaje
            
            idProfesion = profesion.idProfesion
            
            idPersonaje = DatosPersonaje.objects.get(idPersonaje= idPersonaje)
            idProfesion = DatosProfesion.objects.get(idProfesion= idProfesion)          
            
            # Insertamos los registros en la tabla relacional
            Relacion_personaje_profesion.objects.create(idPersonaje=idPersonaje, idProfesion=idProfesion)

            # Para pasar a la creación de la familia
            #creacionFamilia = CrearFamilia()

            return redirect("creacionFamilia")

#            return render(request,"creacionFamilia.html",{"creacion":creacionFamilia,"mensaje" : "Personaje Creado!"})
    else:
        creacion = CrearPj()
    
    return render(request, 'creacionPj.html', {"creacion":creacion})

@login_required
def creacionFamilia(request):
    if request.method == "POST":
        creacion = CrearFamilia(request.POST)
        if creacion.is_valid():
            informacion = creacion.cleaned_data
            # Para Clase Familia
            familia = informacion["familia"]
            antiguedad = informacion["antiguedad"]
            profesionFamilia = informacion["profesionFamilia"][0]
            
            # Chequear si existe objeto guardado
            familia, creado = DatosFamilia.objects.get_or_create(familia=familia,antiguedad=antiguedad,profesionFamilia=profesionFamilia)
            
            ultimoIdFamilia = familia.idFamilia
  
            
            ultimoPj = DatosPersonaje.objects.latest('idPersonaje')
            ultimoIdPersonaje = ultimoPj.idPersonaje
            
            idPersonaje = DatosPersonaje.objects.get(idPersonaje= ultimoIdPersonaje)
            idFamilia = DatosFamilia.objects.get(idFamilia= ultimoIdFamilia)          
            
            # Insertamos los registros en la tabla relacional
            Relacion_personaje_familia.objects.create(idPersonaje=idPersonaje, idFamilia=idFamilia)

                
            return render(request,"inicio.html",{"mensaje" : "Personaje Creado!"})
    else:
        creacion = CrearFamilia()
    
    return render(request, 'creacionFamilia.html', {"creacion":creacion})

@login_required
def busquedaPersonaje(request):
    return render(request, "busquedaPersonaje.html")

@login_required
def buscar(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        personajes = DatosPersonaje.objects.filter(nombre__icontains = nombre)
        return render(request, "resultadosBusqueda.html", {"personajes": personajes})
    else:
        return render(request, "busquedaPersonaje.html", {"mensaje":"Por favor ingrese un nombre"})