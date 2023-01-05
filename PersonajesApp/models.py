from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DatosPersonaje(models.Model):
    idPersonaje = models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50)
    raza=models.CharField(max_length=50)
    edad = models.IntegerField()
    altura = models.FloatField()
    peso = models.IntegerField()
    usuario = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre



class DatosFamilia(models.Model):
    idFamilia = models.AutoField(primary_key=True)
    familia= models.CharField(max_length=50)
    antiguedad = models.CharField(max_length=50)
    profesionFamilia = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.familia
        

class DatosProfesion(models.Model):
    idProfesion = models.AutoField(primary_key=True)
    profesion= models.CharField(max_length=50)
    expertis = models.CharField(max_length=50)
    renombre = models.CharField(max_length=50)
    

    def __str__(self):
        return self.profesion

class Relacion_personaje_familia(models.Model):
    idPersonaje = models.ForeignKey(DatosPersonaje, on_delete=models.CASCADE)
    idFamilia = models.ForeignKey(DatosFamilia, on_delete=models.CASCADE)
    
class Relacion_personaje_profesion(models.Model):
    idPersonaje = models.ForeignKey(DatosPersonaje, on_delete=models.CASCADE)
    idProfesion = models.ForeignKey(DatosProfesion, on_delete=models.CASCADE)
    
class HistoriaPersonaje(models.Model):
    idPersonaje = models.ForeignKey(DatosPersonaje, on_delete=models.CASCADE)
    historia = models.TextField()
    
class AvatarPersonaje(models.Model):
    idPersonaje = models.ForeignKey(DatosPersonaje, on_delete=models.CASCADE)
    avatarPersonaje = models.ImageField(upload_to='avataresPersonajes', null=True, blank = True)
 
    def __str__(self):
        return f"{self.user} - {self.imagen}"