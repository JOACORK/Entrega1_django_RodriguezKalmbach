from django.shortcuts import render, redirect
from PersonajesApp.forms import  CrearFamilia, CrearPj
from PersonajesApp.models import *
from django.contrib.auth.decorators import login_required
from AppPerfiles.views import obtener_avatar
from .funciones_logicas import generar_avatar_personaje, consulta_personajes_sql,consulta_personaje_sql,consulta_admin_personajes_sql,send_message,obtener_avatar_personaje, obtener_info_personaje
import random



def inicio(request):
    return render(request, 'inicio.html',{"avatar":obtener_avatar(request)})

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
    
    return render(request, 'creacionPj.html', {"creacion":creacion,"avatar":obtener_avatar(request)})

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

                
            return render(request,"inicio.html",{"mensaje" : "Personaje Creado!","avatar":obtener_avatar(request)})
    else:
        creacion = CrearFamilia()
    
    return render(request, 'creacionFamilia.html', {"creacion":creacion})

@login_required
def busquedaPersonaje(request):
    return render(request, "busquedaPersonaje.html",{"avatar":obtener_avatar(request)})

@login_required
def buscar(request):
        import time
        
        #time.sleep(4)
        if request.GET["nombre"]:
            #time.sleep(4)
            nombre = request.GET["nombre"]
            #time.sleep(4)
            personajes = DatosPersonaje.objects.prefetch_related(
            'relacion_personaje_profesion_set__idProfesion',
            'relacion_personaje_familia_set__idFamilia'
            ).filter(nombre__icontains=nombre)
            #time.sleep(4)
            
            return render(
                request,
                "resultadosBusqueda.html",
                {
                    "personajes": personajes,
                    "mensaje": "Resultado Búsqueda",
                    "avatar": obtener_avatar(request)
                }
            )
            
        else:
            return render(request, "busquedaPersonaje.html", {"mensaje":"Por favor ingrese un nombre","avatar":obtener_avatar(request)})
    
@login_required
def baulPersonajes(request):
    """
    # Hacer la búsqueda de todos los personajes creados por el usuario
    personajes = DatosPersonaje.objects.filter(usuario=usuario)
    return render(request, "baulPersonajes.html", {"personajes": personajes})
    """
    usuario = request.user
    # Crear la consulta JOIN en lenguaje MySQL
    if request.user.is_superuser:
        resultado = consulta_admin_personajes_sql(usuario)
    else:
        resultado = consulta_personajes_sql(usuario)
        
    filas = []
    for fila in resultado:
        filas.append(fila)

    
    return render(request, "baulPersonajes.html", {"personajes": filas,"avatar":obtener_avatar(request)})

@login_required
def creadorHistoria(request, personaje_id): 
    #TODO Obtener valores del id
    # impactar en gpt3 
     
    usuario = request.user

    consulta_personaje_sql(usuario,personaje_id)
    pass

@login_required
def eliminarPersonaje(request, personaje_id):
    usuario = request.user
    personaje = DatosPersonaje.objects.get(idPersonaje= personaje_id)
   
    personaje.delete()
    
    personajes = DatosPersonaje.objects.all()
    

    resultado = consulta_admin_personajes_sql(usuario)    
    filas = []
    for fila in resultado:
        filas.append(fila)

    
    return render(request, "baulPersonajes.html", {"personajes": filas})
    
    
@login_required
def editarPersonaje(request, personaje_id,profesion_id,familia_id):
    #TODO poder editar personaje
    personaje = DatosPersonaje.objects.get(idPersonaje= personaje_id)
    profesion = DatosProfesion.objects.get(idProfesion= profesion_id)
    if request.method == "POST":
        formulario_personaje = CrearPj(request.POST)
        if formulario_personaje.is_valid():
            
            informacion = formulario_personaje.cleaned_data
            personaje.nombre = informacion["nombre"] 
            personaje.raza= informacion["raza"][0]
            personaje.edad =  informacion["edad"]
            personaje.altura =  informacion["altura"]
            personaje.peso =  informacion["peso"]
            profesion.profesion =  informacion["profesion"][0]
            profesion.expertis =  informacion["expertis"][0]
            profesion.renombre =  informacion["renombre"][0]
            personaje.save()
            profesion.save()
            
        return render(request,"inicio.html",{"mensaje":"Edicion lograda con éxito!"})
    else:
        personaje = CrearPj(initial={"nombre":personaje.nombre,"raza":personaje.raza,"edad":personaje.edad,"altura":personaje.altura,"peso":personaje.peso,"profesion":profesion.profesion,"expertis":profesion.expertis,"renombre":profesion.renombre})
    return render(request,"creacionPj.html",{"creacion":personaje,"avatar":obtener_avatar(request)})


@login_required
def crearHistoria(request, personaje_id):
    '''
    Esta view toma los datos de los personajes creados, y genera un prompt predeterminado.
    Se utiliza un wrapper para hacer peticiones de forma gratuita a la IA-GPT3 --> documentación: https://github.com/terry3041/pyChatGPT/blob/main/README.md
    '''
    personaje = DatosPersonaje.objects.get(idPersonaje= personaje_id)
    
    # Obtener datos de personaje
    profesion_id = Relacion_personaje_profesion.objects.get(idPersonaje_id=personaje_id).idProfesion_id
    profesion = DatosProfesion.objects.get(idProfesion = profesion_id)
    
    #time.sleep(10)
    familia_id = Relacion_personaje_familia.objects.get(idPersonaje_id=personaje_id).idFamilia_id
    familia = DatosFamilia.objects.get(idFamilia = familia_id)

    nombrePersonaje = personaje.nombre
    aniosPersonaje = personaje.edad
    razaPersonaje = personaje.raza
    nombreFamilia = familia.familia
    profesionFamilia = familia.profesionFamilia
    antiguedadFamilia = familia.antiguedad
    profesionPersonaje = profesion.profesion
    expertisPersonaje = profesion.expertis
    
    semilla = random.random()
    prompt_chatGPT3 = f"""Usar semilla: "{semilla}". Estilo de J. R. R. Tolkien. Redactar en 200 palabras la hoja de vida de un personaje ficticio llamado  "{nombrePersonaje}", de raza {razaPersonaje}.Creció en una familia de nombre "{nombreFamilia}" que tiene {antiguedadFamilia} años de antigüedad. Históricamente la familia se dedicó a la {profesionFamilia}. "{nombrePersonaje}" ejerce la profesión de {profesionPersonaje} y tiene un conocimiento {expertisPersonaje}. {nombrePersonaje} tiene {aniosPersonaje} años. Cualidad única al azar, decidir al azar si tiene implicancias negativas, neutras o positivas. Desarrollar introducción y crecimiento del personaje en relación a su pueblo. Finalizar con evento narrativo que de inicio a una aventura."""
    # Chequeo si ya se creo una historia para el personaje
    historia_vieja = HistoriaPersonaje.objects.filter(idPersonaje_id=personaje_id)
    
    
    if len(historia_vieja)!= 0:
        if historia_vieja[0].historia != "Error al crear historia":
            historia = historia_vieja[0].historia
            
            return render(request,"crearHistoria.html",{"personaje":personaje,"historia":historia,"mensaje":"Historia creada con éxito!"})
        else:      
            
            historia_vieja.delete()      
            respuesta_chat, mensaje = send_message(prompt_chatGPT3)
            HistoriaPersonaje.objects.create(idPersonaje_id=personaje_id,historia = respuesta_chat)
            historia = HistoriaPersonaje.objects.filter(idPersonaje_id=personaje_id)[0].historia
            
            return render(request,"crearHistoria.html",{"personaje":personaje,"historia":historia,"mensaje":mensaje})
    else:
        
        respuesta_chat, mensaje = send_message(prompt_chatGPT3)
        HistoriaPersonaje.objects.create(idPersonaje_id=personaje_id,historia = respuesta_chat)
        historia = HistoriaPersonaje.objects.filter(idPersonaje_id=personaje_id)[0].historia
        
    return render(request,"crearHistoria.html",{"personaje":personaje,"historia":historia,"mensaje":mensaje})



@login_required
def crearAvatarPersonaje(request, personaje_id):
    personaje = DatosPersonaje.objects.get(idPersonaje=personaje_id)
    
    profesion_id = Relacion_personaje_profesion.objects.get(idPersonaje_id= personaje_id).idProfesion_id
    profesion = DatosProfesion.objects.get(idProfesion=profesion_id)
    
    familia_id = Relacion_personaje_familia.objects.get(idPersonaje_id=personaje_id).idFamilia_id
    familia = DatosFamilia.objects.get(idFamilia = familia_id)
    
    raza = personaje.raza
    edad = personaje.edad
    profesionPersonaje = profesion.profesion
    
    avatarPersonaje = generar_avatar_personaje(raza,edad,profesionPersonaje)[0]
    AvatarPersonaje.objects.create(idPersonaje=personaje,avatarPersonaje= avatarPersonaje)
    return render(request,"inicio.html",{"mensaje":"Avatar personaje creado!","personaje":personaje,"profesion":profesion,"familia":familia})

def detallePersonaje(request, personaje_id):
    personaje = DatosPersonaje.objects.get(idPersonaje=personaje_id)
    
    profesion_id = Relacion_personaje_profesion.objects.get(idPersonaje_id= personaje_id).idProfesion_id
    profesion = DatosProfesion.objects.get(idProfesion=profesion_id)
    
    familia_id = Relacion_personaje_familia.objects.get(idPersonaje_id=personaje_id).idFamilia_id
    familia = DatosFamilia.objects.get(idFamilia = familia_id)
    
    avatarPersonaje= obtener_avatar_personaje(personaje_id)
    

    
    try:
        historiaPersonaje = HistoriaPersonaje.objects.get(idPersonaje_id = personaje_id)
    except HistoriaPersonaje.DoesNotExist:
        historiaPersonaje = "No se ha creado la historia todavía"
    return render(request,"detallePersonaje.html",{"mensaje":"Avatar personaje creado!","historiaPersonaje":historiaPersonaje,"avatarPersonaje":avatarPersonaje,"personaje":personaje,"profesion":profesion,"familia":familia})