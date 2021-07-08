from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Tu Nombre"
    }))
    apellidos= forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Tus Apellidos"
    }))
    correo_electronico = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': "Tu Correo Electrónico"
    }))
    celular = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': "Tu número de celular",'min': "0"
    }))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Tu Mensaje", 
    }))
    
    