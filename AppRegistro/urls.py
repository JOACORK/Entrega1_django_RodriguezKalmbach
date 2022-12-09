from django.urls import path
from AppRegistro.views import *

urlpatterns = [
    path("accounts/signup/", signup, name="signup"),
]