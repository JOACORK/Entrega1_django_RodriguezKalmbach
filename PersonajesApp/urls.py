from django.urls import path
from PersonajesApp.views import *
from AppRegistro.views import *

urlpatterns = [
    path("", inicio, name="inicio"),
    path("creacionFamilia/", creacionFamilia, name="creacionFamilia"),
    path("creacionPj/", creacionPj, name="creacionPj"),    
    path("busquedaPersonaje/", busquedaPersonaje, name= "busquedaPersonaje"),
    path("baulPersonajes/", baulPersonajes, name= "baulPersonajes"),
    path("buscar/",buscar, name="buscar"),
    path("creadorHistoria/<personaje_id>/",creadorHistoria, name="creadorHistoria"),
    path("eliminarPersonaje/<personaje_id>/",eliminarPersonaje, name="eliminarPersonaje"),
    path("editarPersonaje/<personaje_id>/<profesion_id>/<familia_id>/",editarPersonaje, name="editarPersonaje"),
    
    
    
]