from django.shortcuts import render, redirect
from django.http import HttpResponse
from PersonajesApp.forms import CrearPersonaje, CrearFamilia, CrearPj
from PersonajesApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import time
from django.db import connection
from AppPerfiles.views import obtener_avatar

######## Librerías para IA ###################
from pyChatGPT import ChatGPT
#from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
#import torch
import replicate
import os
import replicate

##############################################
import random

# Funcionesútiles





# Create your views here.


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
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        personajes = DatosPersonaje.objects.filter(nombre__icontains = nombre)
        return render(request, "resultadosBusqueda.html", {"personajes": personajes,"avatar":obtener_avatar(request)})
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
        print("SUPERUSUARIO")
        print(usuario)
        resultado = consulta_admin_personajes_sql(usuario)
    else:
        resultado = consulta_personajes_sql(usuario)
    filas = []
    for fila in resultado:
        filas.append(fila)

    #print(filas[0])
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
    print(personaje)
    personajes = DatosPersonaje.objects.all()
    #print(personajes)

    resultado = consulta_admin_personajes_sql(usuario)    
    filas = []
    for fila in resultado:
        filas.append(fila)

    #print(filas[0])
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
    print("nueva 0")
    
    if len(historia_vieja)!= 0:
        if historia_vieja[0].historia != "Error al crear historia":
            historia = historia_vieja[0].historia
            print("nueva 1")
            return render(request,"crearHistoria.html",{"personaje":personaje,"historia":historia,"mensaje":"Historia creada con éxito!"})
        else:      
            print("nueva 2")
            historia_vieja.delete()      
            respuesta_chat = send_message(prompt_chatGPT3)
            HistoriaPersonaje.objects.create(idPersonaje_id=personaje_id,historia = respuesta_chat)
            historia = HistoriaPersonaje.objects.filter(idPersonaje_id=personaje_id)[0].historia
            print(historia)
            return render(request,"crearHistoria.html",{"personaje":personaje,"historia":historia,"mensaje":"Historia creada con éxito!"})
    else:
        print("nueva 4")
        respuesta_chat = send_message(prompt_chatGPT3)
        HistoriaPersonaje.objects.create(idPersonaje_id=personaje_id,historia = respuesta_chat)
        historia = HistoriaPersonaje.objects.filter(idPersonaje_id=personaje_id)[0].historia
        print(historia)
    return render(request,"crearHistoria.html",{"personaje":personaje,"historia":historia,"mensaje":"Historia creada con éxito!"})



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
    #image.save("astronaut_rides_horse.png")
    return render(request,"inicio.html",{"mensaje":"Avatar personaje creado!","personaje":personaje,"profesion":profesion,"familia":familia})

def detallePersonaje(request, personaje_id):
    personaje = DatosPersonaje.objects.get(idPersonaje=personaje_id)
    
    profesion_id = Relacion_personaje_profesion.objects.get(idPersonaje_id= personaje_id).idProfesion_id
    profesion = DatosProfesion.objects.get(idProfesion=profesion_id)
    
    familia_id = Relacion_personaje_familia.objects.get(idPersonaje_id=personaje_id).idFamilia_id
    familia = DatosFamilia.objects.get(idFamilia = familia_id)
    
    avatarPersonaje= obtener_avatar_personaje(personaje_id)
    print(avatarPersonaje)
    #linkPersonaje = str.split("/",avatarPersonaje)
   # print(linkPersonaje)
    
    historiaPersonaje = HistoriaPersonaje.objects.get(idPersonaje_id = personaje_id)
    
    return render(request,"detallePersonaje.html",{"mensaje":"Avatar personaje creado!","historiaPersonaje":historiaPersonaje,"avatarPersonaje":avatarPersonaje,"personaje":personaje,"profesion":profesion,"familia":familia})

######################### FUNCIONES CON UTILIDAD EN LAS VISTAS ###########################################3

def generar_avatar_personaje(raza,edad,profesionPersonaje):
    lista_razas = {"Humanos":"human", "Orcos":"orc", "Elfos":"elf", "Enanos":"halfling", "Goblins":"goblin", "Trolls":"troll", "Enanos":"dwarf","Medianos":"hobbit"}
    raza_ajustada_prompt = lista_razas[raza]
    """
    model_id = "stabilityai/stable-diffusion-2-base"

    # Usar Euler scheduler
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)

    #pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
    #pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler''', torch_dtype=torch.float16''')
    pipe = pipe.to("cuda")
    pipe.save_pretrained("./models/",safe_serialization=True)
    """
    #model = replicate.models.get("stability-ai/stable-diffusion")
    #version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
    os.environ["REPLICATE_API_TOKEN"] = "952006b617ba2b59a77c40f1a31750d9a8c82ff5"
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
    image = version.predict(prompt=f"Illustration of an {edad} year old {raza_ajustada_prompt}'s face, Tolkien's Middle Earth style.  With the following phrase written at the base of the image: 'Throu, el {profesionPersonaje}'")
    

    return (image)
   



def consulta_personajes_sql(usuario):
        # Crear la consulta JOIN en lenguaje MySQL
    consulta = f"""
        SELECT a.idPersonaje,a.nombre,a.raza,a.edad,e.profesion,e.expertis,e.renombre,c.familia,c.antiguedad,c.profesionFamilia,e.idProfesion, c.idFamilia
        FROM PersonajesApp_datospersonaje as a
        INNER JOIN PersonajesApp_relacion_personaje_familia as b ON a.idPersonaje = b.idPersonaje_id
        INNER JOIN PersonajesApp_datosfamilia as c ON b.idFamilia_id = c.idFamilia 
        INNER JOIN PersonajesApp_relacion_personaje_profesion as d on a.idPersonaje = d.idPersonaje_id
        INNER JOIN PersonajesApp_datosprofesion as e on d.idProfesion_id = e.idProfesion
        WHERE a.usuario = '{usuario}';"""
        
    # Ejecutar la consulta y obtener el resultado
    resultado = connection.cursor().execute(consulta)
    
    return resultado
        
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

def send_message(prompt: str):
    '''
    Recibe texto en formato string, hace una petición a la API de GPT3 y 
    devuelve texto creado
    '''
    # Este token se obtiene siguiendo los pasos detallados del siguiente link https://github.com/terry3041/pyChatGPT/blob/main/README.md
    #1- Go to https://chat.openai.com/chat and open the developer tools by F12.
    #2- Find the __Secure-next-auth.session-token cookie in Application > Storage > Cookies > https://chat.openai.com.
    #3- Copy the value in the Cookie Value field.
    
    session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..sUH8TQQHZVoM_azL.R8b8SQPSUloUji0vf5S8MHktr-SOjhMjJ8omQrT8W0xsjMx46j3y9bA4jWTl3XVCePSVxNB0UhuwMhDLTnhiyAKp4eBDweqrRYhGqojJ3TodBgvlI3cSGejfzNdYV6PuYM2fKipD2-8lxNuqWbHIMc_1aj1ZbZCIAe2rEm9TtdFuhU-gJha_Wc2g_g_tV9xU28eyBtASfntc9CEc3SzoMtDMhw_4YFezhusCJZ90A-CAGOUycptZIscmvhb2RNcTERiAgZ2Nx4uKCIKZYGdaA6ktQi7wHMiarUl--vTP4A1zZmqxMmFSwAM1pm2bYWZCcqMvjSQWFOGYc3enW_K3jSU2p8scdAQ85RSJSd0cyZbFUj2bpQ75LKTCCK5CaeChf_VNTbnB5aInqoJZwUcrAxZrRltUP7cD60FF_ltvC7TgJIUPx1tpp81MVe0KK9bwgRz-7YFJTmf0dtokr5tZ-XkJH4YjNHtrt1IswiUko6AePsU1P6xVyaYvNK8S6J82itLJ-PMWf34-aluvgWdwAqLRuYYwmnY2ty4jRX9mz2Xm0H1j7L0fC8_xq99_yHvUYzL9Awv4lKCsBQEiQisxZ1zg6_1dkyMUqXOVoxnY4jUl2sPoXj7HBSiOmQyGl7beqGAy_m_PsDtpBPtcPqQvHqhd4037dCCUwz330MJpxX81OSI5hUotojgx98WXqdRNRwMAFbZtMe4jnGY-ojeP26e81lPy2HwqC9jnZ-qfP0_t2OZ6Qlft3CGLdqiHpUmEQHmLut-j_6sAwkApkNlx3lOb1dAQBGjCzI3bZQiSkV2utIMjZ6FbhWmNFMW-dC080j31X7Eb9-2cOJsjBmXzkt0BSFsfsknewPdkFspTURkm2T6rZCqd8ed0Yt1xs7ZGQArSxIIOO9EnTaUmzh9fhUdLcXuNs9FU5eqdN58gZ_2SBo3-V5g4ZyUqjrbvj9ZyFG07nXGeZUBopt-OtMB4c6feGjUma0_YTxgmfvEux8WsT52I__d8MMaMWvURgLfm-Y_5A1qNg0yt6xAk-bKSNdLJwVzA80QPTxnHr00sagZNw_XBwosJolEqomexY4XSmYmIgYBT_qQCjgAGvvDHpd_2SUGGYgW4CltZyx95jddJNTLJ0M6pTpfozdJN4BUqZt_DzK8g225_eet4fml8FNOh5bK8ojlEAsAY9d6DzvZFZyl54yJ5vye3AqZ8Tllk5UpPuT3yan4s43Ngy0oa6-Xc6M3Zlyt5iGwrsaPSEcUeJEBfMW3TwOdNpVD45b0klvadzILnMWfLdZ33SlX1kzfcvA6xSSDEbdm27PwJ0kbKPN9kyxytWZUrY8jX4A_j6xiq49pXkBsDUbiz99q9bvMFiMisOUgBQYPosQNSWZ1IOlOTY8FcRaEBwAbvif8mlKt8IZJUScPdyjXp-7izN213gsDDBTWymyqyU5W7-1zL9tFIfmloOKkfKro0aMjYBMthWFm4bD3e8HFiPPpzUKaJzHQVmu_bit01nGDPR3uO5TiZYC0nyH6K7PnDO7iXBDxS4ntYlm6P10YtXSmu4T0YQ1bztyTXHzYAFOGLKgXzc4dt2bquU7SxGPrxv_SSTFFka5w6vI0y53zUx8OztxeHorIztIiIWbS8kvsJNzz1O4Qy_pysxJl_W0zzYUpRzmUxi3_kHeN5bszRwhqk-VAx5yiYAVxHEPvuTSjAlPDKtNlbZQMOF_nhbG_9SWLRx5op9b1yWAV7nYiRNoG9TVvvWSK3tXmZqP6ku359e8UihldfE3eaHyVmtIer1V-l95oFE6DrWfnC58IIBKOGNVbNCwCL4orwRko9gAoXFZga8w3shrMPuuirYd5X-DvR0nsShk-_8aff3wCfgXd-QSjP8qsCSrbtdLeORt06ymHCaVRtJF6vOw6L_-EPQUxlkUWCMdNb_N2VfTfBPXaDMoXTKeQ1_yTa_gI_JAxzVVNAw1EXv_d6ij38IbutsulDqwgmcw8uPX35p3gAIA4q1qKt25lQlJhsIBGJGK_RJfvgNmHVeoRP40iP77SfoJyLBK8O4D3wymUOY3dLPMctX31e6_BhJD0uUdKYfW8GwcRVp-tqHObCJy2p0GoldqyCPB__o7yTTVVRrSqPdxynr4-WxwyrituCjmb2W1AHpfhQADO3vmP08vq_P1jrS97XtEGPBC4vVQA-ghMjtmeN5xrSKG04F31Ol2gIzMEmnITRS_8fhyQO0dECZvcMww7m1udbs11qOAUzX0VCKFCMwqeYyOs.fnmPrQIsU-p5Gil4JtrrXg'
    
    try:
        api = ChatGPT(session_token)
        resp = api.send_message(prompt)
    except:
        resp= {"message":"Error al crear historia"}

    return (resp["message"])

def obtener_avatar_personaje(idPersonaje):
    lista = AvatarPersonaje.objects.filter(idPersonaje_id=idPersonaje)
    if len(lista)!= 0:
        imagen=lista[0].avatarPersonaje
    else:
        imagen="http://clipart-library.com/images_k/silhouette-head-shot/silhouette-head-shot-18.jpg"
    return imagen