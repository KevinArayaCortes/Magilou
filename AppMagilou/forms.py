from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario

class RegistroForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label="Contraseña",
        max_length=255
    )
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}),
        label="Confirmar Contraseña",
        max_length=255
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'correo', 'direccion', 'telefono', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'rut': forms.TextInput(attrs={'placeholder': 'RUT'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")

        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            self.add_error('confirmar_contrasena', "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            usuario.save()
        return usuario
