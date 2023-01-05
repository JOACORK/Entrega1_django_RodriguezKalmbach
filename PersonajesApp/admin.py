from django.contrib import admin
from .models import *
from AppPerfiles.models import *

# Register your models here.

admin.site.register(DatosPersonaje)
admin.site.register(DatosFamilia)
admin.site.register(DatosProfesion)
admin.site.register(Relacion_personaje_familia)
admin.site.register(Relacion_personaje_profesion)
admin.site.register(Avatar)




