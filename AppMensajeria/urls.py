from django.urls import path
from AppMensajeria.views import *

urlpatterns = [
    path("mensajeria/", mensajeria, name="mensajeria"),   
    path("enviar_mensaje/", enviar_mensaje, name="enviar_mensaje"),   
    path("leer_mensajes/", leer_mensajes, name="leer_mensajes"), 
    path("eliminar_mensajes/<id>/", eliminar_mensajes, name="eliminar_mensajes"),   
    path("responder_mensajes/<usuario>/", responder_mensajes, name="responder_mensajes"),   
    
]