from  django import forms
OPCIONES_RAZAS =[("Humanos","Humanos"),("Orcos","Orcos"),("Elfos","Elfos"),("Medianos","Medianos"),("Goblins","Goblins"),("Trolls","Trolls"),("Enanos","Enanos")]
OPCIONES_PROFESIONES_PJ = [("Herrería","Herrería"),("Guerrero","Guerrero"),("Cocinero","Cocinero"),("Noble","Noble"),("Cazador","Cazador")]
OPCIONES_PROFESIONES_FAMILIA = [("Herrería","Herrería"),("Guerreros","Guerreros"),("Cocineros","Cocineros"),("Nobleza","Nobleza"),("Cazadores","Cazadores")]
OPCIONES_EXPERTIS = [("Novato","Novato"),("Conocedor","Conocedor"),("Maestro","Maestro")]
OPCIONES_RENOMBRE = [("Bajo","Bajo"),("Alto","Alto")]

class CrearPersonaje(forms.Form):
    nombre = forms.CharField(max_length=50)
    raza=forms.MultipleChoiceField(choices = OPCIONES_RAZAS)
    edad = forms.IntegerField()
    altura = forms.FloatField()
    peso = forms.IntegerField()
    profesion = forms.MultipleChoiceField(choices = OPCIONES_PROFESIONES_PJ)
    expertis = forms.MultipleChoiceField(choices = OPCIONES_EXPERTIS)
    renombre = forms.MultipleChoiceField(choices = OPCIONES_RENOMBRE)
    familia = forms.CharField(max_length=50)
    antiguedad = forms.IntegerField(help_text="Años de existencia de la familia")
    profesionFamilia = forms.MultipleChoiceField(choices = OPCIONES_PROFESIONES_FAMILIA)
    
class CrearPj(forms.Form):
    nombre = forms.CharField(max_length=50)
    raza=forms.MultipleChoiceField(choices = OPCIONES_RAZAS)
    edad = forms.IntegerField()
    altura = forms.FloatField()
    peso = forms.IntegerField()
    profesion = forms.MultipleChoiceField(choices = OPCIONES_PROFESIONES_PJ)
    expertis = forms.MultipleChoiceField(choices = OPCIONES_EXPERTIS)
    renombre = forms.MultipleChoiceField(choices = OPCIONES_RENOMBRE)

class CrearFamilia(forms.Form):
    familia = forms.CharField(max_length=50)
    antiguedad = forms.IntegerField(help_text="Años de existencia de la familia")
    profesionFamilia = forms.MultipleChoiceField(choices = OPCIONES_PROFESIONES_FAMILIA)

class CrearHistoria(forms.Form):
        id_personaje = forms.CharField(max_length=50)
        nombre = forms.CharField(max_length=50)
        raza = forms.CharField(max_length=50)
        edad = forms.CharField(max_length=50)
        altura = forms.CharField(max_length=50)
        peso = forms.CharField(max_length=50)
        id_familia = forms.CharField(max_length=50)
        familia = forms.CharField(max_length=50)
        antiguedad = forms.CharField(max_length=50)
        profesion_familia = forms.CharField(max_length=50)
