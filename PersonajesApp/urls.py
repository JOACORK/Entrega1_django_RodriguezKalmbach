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
    path("creadorHistoria/",creadorHistoria, name="creadorHistoria"),
    
]