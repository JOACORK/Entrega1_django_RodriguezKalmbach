from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MensajeForm
from AppMensajeria.models import *
from django.contrib.auth import get_user_model
import time

# Create your views here.
@login_required
def mensajeria(request):
    form = MensajeForm()
    return render(request,"mensajeria.html",{"form":form})

@login_required
def enviar_mensaje(request):
    
    if request.method == "POST":
        remitente = request.user
        print(remitente)
        #time.sleep(4)
        destinatario = request.POST['destinatario']
        print(destinatario)
        cuerpo = request.POST['cuerpo']
               
        existe_destinatario = User.objects.filter(username= destinatario)
        
        form=MensajeForm()
        if existe_destinatario:
            
            mensaje = Mensaje(remitente=remitente, destinatario=destinatario, cuerpo=cuerpo)
            mensaje.save()
            
            return render(request, 'mensajeria.html', {'form':form,'mensaje': f"Mensaje enviado correctamente al usuario {destinatario}!"})
        else:
            return render(request, 'mensajeria.html', {'form':form,'mensaje': f"Error al enviar mensaje {destinatario} no es un usuario de la plataforma"})

    
    else:
        form=MensajeForm()
        return render(request, 'mensajeria.html',{'form':form,'mensaje': "Error al enviar mensaje"})


@login_required
def leer_mensajes(request):
    mensajes = Mensaje.objects.filter(destinatario=request.user.username)
    for mensaje in mensajes:
        mensaje.mensaje_leido = True
        mensaje.save()
    return render(request, 'buzon_mensajes.html', {'mensajeria': mensajes})

def eliminar_mensajes(request, id):
    msg_a_borrar = Mensaje.objects.get(id= id)
   
    msg_a_borrar.delete()
    
    mensajes = Mensaje.objects.filter(destinatario=request.user.username)    
    return render(request, "buzon_mensajes.html", {"mensajeria": mensajes})

def responder_mensajes(request,usuario):   
    print(usuario)
    form = MensajeForm(initial={"destinatario":usuario})
    return render(request,"mensajeria.html",{"form":form})