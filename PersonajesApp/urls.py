from django.urls import path
from PersonajesApp.views import *

urlpatterns = [
    path("", inicio, name="inicio"),
    path("creacion/", creacion, name="creacion"),

]