from django.db import models

# Create your models here.

class DatosPersonaje(models.Model):
    nombre=models.CharField(max_length=50)
    raza=models.CharField(max_length=50)
    edad = models.IntegerField()
    altura = models.FloatField()
    peso = models.IntegerField()
    def __str__(self):
        return self.nombre



class DatosFamilia(models.Model):
    familia= models.CharField(max_length=50)
    antiguedad = models.CharField(max_length=50)
    profesionFamilia = models.CharField(max_length=50)

    def __str__(self):
        return self.familia
        

class DatosProfesion(models.Model):
    profesion= models.CharField(max_length=50)
    expertis = models.CharField(max_length=50)
    renombre = models.CharField(max_length=50)
    

    def __str__(self):
        return self.profesion
