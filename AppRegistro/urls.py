from django.urls import path
from AppRegistro.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("accounts/signup/", signup, name="signup"),
    path("accounts/login/", login_request, name="login"),
    path("accounts/logout/", LogoutView.as_view(template_name="logout.html"),name="Logout"),    
]