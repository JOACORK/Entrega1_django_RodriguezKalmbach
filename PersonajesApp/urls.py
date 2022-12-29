from django.urls import path
from PersonajesApp.views import *
from AppRegistro.views import *

urlpatterns = [
    path("", inicio, name="inicio"),
    path("creacion/", creacion, name="creacion"),
    path("busquedaPersonaje/", busquedaPersonaje, name= "busquedaPersonaje"),
    path("buscar/",buscar, name="buscar"),
]