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
            return redirect("creacionFamilia")

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
    if request.user.is_superuser:
        resultado = consulta_admin_personajes_sql(usuario)
    else:
        resultado = consulta_personajes_sql(usuario)
    filas = []
    for fila in resultado:
        filas.append(fila)

    #print(filas[0])
    return render(request, "baulPersonajes.html", {"personajes": filas})

def creadorHistoria(request, personaje_id): 
    #TODO Obtener valores del id
    # impactar en gpt3 
     
    usuario = request.user

    consulta_personaje_sql(usuario,personaje_id)
    pass

def eliminarPersonaje(request, personaje_id):
    usuario = request.user
    personaje = DatosPersonaje.objects.get(idPersonaje= personaje_id)
   
    personaje.delete()
    print(personaje)
    personajes = DatosPersonaje.objects.all()
    #print(personajes)

    resultado = consulta_admin_personajes_sql(usuario)    
    filas = []
    for fila in resultado:
        filas.append(fila)

    #print(filas[0])
    return render(request, "baulPersonajes.html", {"personajes": filas})
    
    

def editarPersonaje(request, personaje_id,profesion_id,familia_id):
    #TODO poder editar personaje
    personaje = DatosPersonaje.objects.get(idPersonaje= personaje_id)
    profesion = DatosProfesion.objects.get(idProfesion= profesion_id)
    familia = DatosFamilia.objects.get(idFamilia = familia_id)
    if request.method == "POST":
        formulario_personaje = CrearPj(request.POST)
        if formulario_personaje.is_valid():
            
            informacion = formulario_personaje.cleaned_data
            personaje.nombre = informacion["nombre"] 
            personaje.raza= informacion["raza"]
            personaje.edad =  informacion["edad"]
            personaje.altura =  informacion["altura"]
            personaje.peso =  informacion["peso"]
            profesion.profesion =  informacion["profesion"]
            profesion.expertis =  informacion["expertis"]
            profesion.renombre =  informacion["renombre"]
            familia.familia = informacion["familia"]
            familia.idFamilia =informacion["idFamilia"]
            familia.antiguedad = informacion["antiguedad"]
            familia.profesionFamilia=informacion["profesionFamilia"] 
            personaje.save()
            profesion.save()
            
            formulario_familia = CrearFamilia(initial={"familia": familia.familia,"antiguedad":familia.antiguedad,"profesionFamilia":familia.profesionFamilia})
        return render(request,"creacionFamilia.html",{"creacion":formulario_familia})
    else:
        personaje = CrearPj(initial={"nombre":personaje.nombre,"raza":personaje.raza,"edad":personaje.edad,"altura":personaje.altura,"peso":personaje.peso,"profesion":profesion.profesion,"expertis":profesion.expertis,"renombre":profesion.renombre})
    return render(request,"creacionPj.html",{"creacion":personaje})


def consulta_personaje_sql(usuario,idPersonaje):
        # Crear la consulta JOIN en lenguaje MySQL
    consulta = f"""
        SELECT a.idPersonaje,a.nombre,a.raza,a.edad,e.profesion,e.expertis,e.renombre,c.familia,c.antiguedad,c.profesionFamilia,e.idProfesion, c.idFamilia
        FROM PersonajesApp_datospersonaje as a
        INNER JOIN PersonajesApp_relacion_personaje_familia as b ON a.idPersonaje = b.idPersonaje_id
        INNER JOIN PersonajesApp_datosfamilia as c ON b.idFamilia_id = c.idFamilia 
        INNER JOIN PersonajesApp_relacion_personaje_profesion as d on a.idPersonaje = d.idPersonaje_id
        INNER JOIN PersonajesApp_datosprofesion as e on d.idProfesion_id = e.idProfesion
        WHERE a.usuario = '{usuario}' and a.idPersonaje = '{idPersonaje}';
    """

    # Ejecutar la consulta y obtener el resultado
    resultado = connection.cursor().execute(consulta)
    
    return resultado

def consulta_admin_personajes_sql(usuario):
        # Crear la consulta JOIN en lenguaje MySQL
    consulta = f"""
        SELECT a.idPersonaje,a.nombre,a.raza,a.edad,e.profesion,e.expertis,e.renombre,c.familia,c.antiguedad,c.profesionFamilia,a.usuario, e.idProfesion, c.idFamilia
        FROM PersonajesApp_datospersonaje as a
        INNER JOIN PersonajesApp_relacion_personaje_familia as b ON a.idPersonaje = b.idPersonaje_id
        INNER JOIN PersonajesApp_datosfamilia as c ON b.idFamilia_id = c.idFamilia 
        INNER JOIN PersonajesApp_relacion_personaje_profesion as d on a.idPersonaje = d.idPersonaje_id
        INNER JOIN PersonajesApp_datosprofesion as e on d.idProfesion_id = e.idProfesion
        ;
    """

    # Ejecutar la consulta y obtener el resultado
    resultado = connection.cursor().execute(consulta)
    
    return resultado