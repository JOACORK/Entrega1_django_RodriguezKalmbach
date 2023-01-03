from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Mensaje(models.Model):
    remitente = models.CharField(max_length=50)
    destinatario = models.CharField(max_length=50)
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
