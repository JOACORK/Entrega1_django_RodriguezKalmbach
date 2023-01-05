from django.urls import path
from AppPerfiles.views import editarPerfilUsuario, perfilUsuario, cargarAvatar

urlpatterns = [
    path("accounts/profile/editarPerfilUsuario/", editarPerfilUsuario, name="editarPerfilUsuario"),
    path("accounts/profile/", perfilUsuario, name="perfilUsuario"),
    path("accounts/profile/cargarAvatar",cargarAvatar, name="cargarAvatar"),
    
    ]
