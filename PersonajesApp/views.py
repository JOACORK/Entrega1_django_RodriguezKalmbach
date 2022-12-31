from django.shortcuts import render, redirect
from django.http import HttpResponse
from PersonajesApp.forms import CrearPersonaje, CrearFamilia, CrearPj
from PersonajesApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import time
from django.db import connection



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
            usuario = request.user
            #nombre_usuario = usuario.first_name

            #print(usuario)
            
            #time.sleep(10)

            # Crea personaje y profesion            
            personaje, creado = DatosPersonaje.objects.get_or_create(nombre=nombre,raza= raza, edad = edad,  altura = altura,peso = peso,usuario=usuario)

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
    
    
def baulPersonajes(request):
    # Obtener el usuario que ha generado la solicitud
    usuario = request.user
    """
    # Hacer la búsqueda de todos los personajes creados por el usuario
    personajes = DatosPersonaje.objects.filter(usuario=usuario)
    return render(request, "baulPersonajes.html", {"personajes": personajes})
    """
    # Crear la consulta JOIN en lenguaje MySQL
    consulta = f"""
        SELECT a.idPersonaje,a.nombre,a.raza,a.edad,e.profesion,e.expertis,e.renombre,c.familia,c.antiguedad,c.profesionFamilia
        FROM PersonajesApp_datospersonaje as a
        INNER JOIN PersonajesApp_relacion_personaje_familia as b ON a.idPersonaje = b.idPersonaje_id
        INNER JOIN PersonajesApp_datosfamilia as c ON b.idFamilia_id = c.idFamilia 
        INNER JOIN PersonajesApp_relacion_personaje_profesion as d on a.idPersonaje = d.idPersonaje_id
        INNER JOIN PersonajesApp_datosprofesion as e on d.idProfesion_id = e.idProfesion
        WHERE a.usuario = '{usuario}'
    """

    # Ejecutar la consulta y obtener el resultado
    resultado = connection.cursor().execute(consulta)
    
    filas = []
    for fila in resultado:
        filas.append(fila)

    #print(filas[0])
    return render(request, "baulPersonajes.html", {"personajes": filas})

def creadorHistoria(request): 
    #TODO CREAR VISTA EN DONDE PUEDA ENVIAR LOS DATOS DE UNA FILA Y DESPUES ENVIAR A CREAR UNA HSITORIA sino enviar el prompt cuando se crea el personaje ya horrarme este paso       
    if request.method == "POST":
        creacion = creadorHistoria(request.POST)
        if creacion.is_valid():
            informacion = creacion.cleaned_data
            print(informacion)
            """id_personaje = request.POST.get('id_personaje')
            nombre = request.POST.get('nombre')
            raza = request.POST.get('raza')
            edad = request.POST.get('edad')
            altura = request.POST.get('altura')
            peso = request.POST.get('peso')
            id_familia = request.POST.get('id_familia')
            familia = request.POST.get('familia')
            antiguedad = request.POST.get('antiguedad')
            profesion_familia = request.POST.get('profesion_familia')"""
        
        return render(request, "creadorHistoria.html", {"nombre": nombre})

    else:
        nombre="get"
    return render(request, "creadorHistoria.html", {"nombre": nombre})
