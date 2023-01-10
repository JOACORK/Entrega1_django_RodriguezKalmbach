from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AppPerfiles.forms import EdicionUsuarioForm, AvatarForm
from AppPerfiles.models  import Avatar
from django.contrib.auth.models import User
# Create your views here.

@login_required
def perfilUsuario(request):
    usuario = request.user
    
    return render(request, "perfilUsuario.html",{"usuario":usuario,"avatar":obtener_avatar(request)})
# Vista de editar el perfil
@login_required
def editarPerfilUsuario(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = EdicionUsuarioForm(request.POST)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.last_name = informacion['last_name']
            usuario.first_name = informacion['first_name']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']

            usuario.save()

            return render(request, "inicio.html")

    else:

        miFormulario = EdicionUsuarioForm(initial={'email': usuario.email,'last_name':usuario.last_name,"first_name":usuario.first_name})

    return render(request, "editarPerfilUsuario.html", {"miFormulario": miFormulario, "usuario": usuario})

@login_required
def cargarAvatar(request):
    if request.method == "POST":
        miFormulario = AvatarForm(request.POST,request.FILES)
        if miFormulario.is_valid():
            
            avatarViejo = Avatar.objects.filter(user_id=request.user.id)
            if len(avatarViejo) != 0:
                avatarViejo.delete()

            avatar= Avatar(user=request.user,imagen=request.FILES["imagen"])        
            
            avatar.save()
            return render(request,"inicio.html",{"mensaje":"Avatar agregado correctamente!"})
    else:
        miFormulario= AvatarForm()
        
    return render(request,"cargarAvatar.html", {"miFormulario": miFormulario,"usuario":request.user,"avatar":obtener_avatar(request)})


def obtener_avatar(request):
    
    if request.user.is_authenticated:    

        lista = Avatar.objects.filter(user=request.user)
        
        if len(lista)!= 0:
            imagen=lista[0].imagen.url
        else: 
            imagen = "http://clipart-library.com/images_k/silhouette-head-shot/silhouette-head-shot-18.jpg"
            
            
    else:
        imagen= "http://clipart-library.com/images_k/silhouette-head-shot/silhouette-head-shot-18.jpg"
    return imagen