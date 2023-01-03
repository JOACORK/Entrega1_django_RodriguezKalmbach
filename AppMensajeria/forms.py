from  django import forms

class MensajeForm(forms.Form):
    destinatario = forms.CharField(max_length=100)
    cuerpo = forms.CharField(widget=forms.Textarea)

    