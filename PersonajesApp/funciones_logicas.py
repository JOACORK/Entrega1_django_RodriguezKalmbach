from django.db import connection
from PersonajesApp.models import *
######## Librerías para IA ###################
from pyChatGPT import ChatGPT
#from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
#import torch
from pathlib import Path
import os
import replicate

def generar_avatar_personaje(raza,edad,profesionPersonaje):
    lista_razas = {"Humanos":"human", "Orcos":"orc", "Elfos":"elf", "Enanos":"halfling", "Goblins":"goblin", "Trolls":"troll", "Enanos":"dwarf","Medianos":"hobbit"}
    raza_ajustada_prompt = lista_razas[raza]
    """
    model_id = "stabilityai/stable-diffusion-2-base"

    # Usar Euler scheduler
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)

    pipe = pipe.to("cuda")
    pipe.save_pretrained("./models/",safe_serialization=True)
    BASE_DIR = Path(__file__).resolve().parent.parent
    model_path = os.path.join(BASE_DIR, 'models')
    model_index_path = "stabilityai/stable-diffusion-2-base"
    scheduler = EulerDiscreteScheduler.from_pretrained(model_path, subfolder="scheduler")
    #pipe = StableDiffusionPipeline.from_pretrained(model_index_path,local_files_only=True,scheduler=scheduler, torch_dtype=torch.float16)
    print("scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_path, scheduler=scheduler, torch_dtype=torch.float16)

    print("pipe")
    prompt=f"Illustration of an {edad} year old {raza_ajustada_prompt}'s face, Tolkien's Middle Earth style.  With the following phrase written at the base of the image: 'Throu, el {profesionPersonaje}'"
    #print("prompt")
    #image = pipe(prompt)[0]
    print("image")
    """

    

    # VERSION PARA REPLICATE
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
    
    session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..kqo5ZCXAMm8DybLL.fzaA7hYVRy0YnaifHHereQtMZrd59-kYQGSp6JG_r7BbQwmgB8jgc20fFma8Qrv3g6QLwVjC5EzG5PRF_9Ye_gI2Pk9UkE2Z04oNe1sZb8qnEaSUnks3Pq2kIfA5RV2fEiM7hW4uROyNSXj6y6hAP7p_d9E8RF_XeXVsYb8S7PKmwpdbsJunUyvFJqKX6dU-h8qWM44cwzJr7bDscpolvMwbzTGMfIR1pV27GcZoyv5zV9O94nuN-KfiILXYuwtVd8QUGsz84l4sMracvufX9TAr-6bCzSzdYW3EtKy7JBzdABPpB5ytYR8fbbC0Wkt7s0MlaX3yG7N9qz672CSXbK2nElAhqxJdMDbBkD0PeWlPj0QNgK31aHVkZqKwYX-dE1QcbUY9eKZFUSJCQa51q-Bu3GFadpmSKS81igR6wtWMyTaoyoJAwFLpCwHUh-vpMB5T364t4WIMFPX8cSufoXenPV6iFwZ7h591fzmBrGENQenJi25k9aAy5JTD5iMM1BDoLK_z_Gv_wgBzWFdOlg_7_Hlf0PxrtdSp_K9vxAKRfWBMzI-5O6isNDU7F-QjE1pgwYVr6RzB6ziE7Mgb1AT0QG3AP5DhB_1OuehFASChn_BMzR9MeCvS0YpPOCmOtnW6jfoUoHiyDg9yqxR8fWdVrWfnlhOz0ypfgWBEl0m5KpwzhCXDD6rTjPu9TJT0btXEnuvoysmSRc179h_W9xZ_07KHc3yzR-QmUyEU9JcWRMflFs6oHRDTg7g4a4gIMZfrAto_-HC79U2ErZbenw0Y8ZAnlvcjTnPpMVzGKCDUDnlmXQSPFQA-PilOTr7ouCOymYvHGYooqhNQHehrmYiOgdAqr-rC4OxEJMI85QLa06E2HjtlziR4NwBKV2_iZ6QYZyTmPEH77LpcREBkQdngyPp3vgIOKRaLvyibMMNTUb9Vh6AW2vIgsImquSPiAjjucNIYtNapBsqkoOfnZ-BW5tlFwPEa-ntiI6lM1wLM5l87PsDH8dS-zn_5glVHiJBjUWUd7Tq6819D8p9rm_ienSG3kdOY8mZXkK5OAmPOJE1btV8U4l2DHBAUdiaw8VDwr9PlAxO-4_d08Mod_bDrvvJrzoLL2NpFA40TFBsMhhKtNrSz9GrWnMHzkh5TVcaWOZsKPWGfOcPOc083wFGP3tOGQgIsP8nm61dabt8Hx-EzdObC7yal3ywJyamojTh7wOxzm_7DJsaD1u2M5ssbZN7q9pxD7RLJYLBGx33XYVPvisWho2mVF8y9Aah0gAZGGHBvh-kS7aYW_7aOaLPhKXsiOBbypNEC2SdDQF4j14J2xQ9Hnf_DiSbsN-8sqITe9yJUPIhUahjS8yGGoWCyS2q_7tMbD78Ia0w6CswydOffoMu5JyBEQ_rpiFjuGr7dYOBLhFt_NCCyoIezv4S8_Fmuw_GLb5bg3_udSQsZGCgZhWL6DSO8J6RnJEg5MOQlFUEo0bY9OU99sABXSHB4In2_H3P2fs4rV4iMSxHesWC2jT-pxQUlwark59Ihx_OX_dQawjPT6ICYemaNXNUs_dN82B7yjawpkfv4HxT3LbAJSsZ_sBsyIhXRDwSi-85IRhGLKK2C5s7whiUpM8Gua6Jh5uBw_OkXkEWbC3slkj0GV6AKig-xb9y2_FAoVr7yLAyYKKPBt8VoGi6sbF655hg6qkOuldhmq6ytOI_cVkkibeLOcKm-a0FTPUdZo6Itek0idZKn6ZTeeh1byYeg_F8_fRqgLXlTvY-4H98UfCQ7lhmR5PSitWHbs-1Kzd4BFN85frHlTp-xZsGAutb4qor4Rb_0tBOoxBzvMPRB_YNK7pnAaVlrAlAB7IPMkVwk3gANHoHJb2IGTqV6IG9LMi36TlfmOdjoe4jsUKVmlfBW3D9YXnoUMcNrqaHcOOUBF7Dm86s8KQbXdniCS1du05G9J6TA-bQoQT-BgAhdCIUjPMzAxbuXIir80KV8V88432Mt6ZFdi19hUI0VzFD4E93c2xecWflkhJlvUbeGNJDXd6KsQIDztXcwV_-xPKaE9mQ7H8A79_xERamvLb3KhMDY8eKbnv4MMHGljwmJQzIfCzvgJNedtj1IZ4C6vB6DtLIOsaYarF7KXoJE1uFxyEbL5e2dx-wXIuwxBY4LQn6TitUvJdvZYbxvWKAWW7eL1WfaS_aqj6G3CH6VvTrrBfk9J8tIeTzmX3n4XCa3hgzb_V2g68FfIik-yJfRSJcm4ruZY_a1VKlEZCjCSLKc35Q.klJKB-5rtPKsnC0wAJqsmQ'
    
    try:
        api = ChatGPT(session_token)
        resp = api.send_message(prompt)
        mensaje_html = "Exito al crear historia!"
    except:
        resp= {"message":"Error al crear historia"}
        mensaje_html = "Error al crear historia"
    return (resp["message"],mensaje_html)

def obtener_avatar_personaje(idPersonaje):
    lista = AvatarPersonaje.objects.filter(idPersonaje_id=idPersonaje)
    if len(lista)!= 0:
        imagen=lista[0].avatarPersonaje
    else:
        imagen="http://clipart-library.com/images_k/silhouette-head-shot/silhouette-head-shot-18.jpg"
    return imagen

def obtener_info_personaje(idPersonaje):
    personaje = DatosPersonaje.objects.get(idPeronaje = idPersonaje)
    
    idFamilia = Relacion_personaje_familia.objects.get(idPersonaje_id = idPersonaje).idFamilia_id
    idProfesion = Relacion_personaje_profesion.objects.get(idPersonaje_id = idPersonaje).idProfesion_id
    familia = DatosFamilia.objects.get(idFamilia = idFamilia)
    profesion = DatosProfesion.objects.get(idProfesion=idProfesion)
    
    historiaPersonaje= HistoriaPersonaje.objects.get(idPersonaje_id=idPersonaje)
    avatarPersonaje = AvatarPersonaje.objects.get(idPersonaje_id=idPersonaje)
    
    return(personaje,familia,profesion,historiaPersonaje,avatarPersonaje)
    