from django import forms
from django.contrib.auth import authenticate
from .models import User

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Contraseña"
            }
        )
    )
    
    password2 = forms.CharField(
        label="contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Repetir contraseña"
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "nombres",
            "apellidos",
            "genero",
        )
    
    def clean_password2(self):
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            self.add_error("password2", "Las contraseñas no son identicas")

class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "username",
                "style" : "{margin: 10px}",
            }
        )
    )
       
    password = forms.CharField(
        label="contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Contraseña"
            }
        )
    )
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        
        if not authenticate(username = username, password = password):
            raise forms.ValidationError("Los datos de usuario no son correctos")
        
        return self.cleaned_data
    
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label="contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Contraseña actual"
            }
        )
    )
    
    password2 = forms.CharField(
        label="contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "contraseña nueva"
            }
        )
    )

class VerificationCodeEmail(forms.Form):
    codregistro = forms.CharField(required=True)
    
    def __init__(self, pk,  *args, **kwargs):
        self.id_user = pk
        super(VerificationCodeEmail, self).__init__(*args, **kwargs)
    
    def clean_codregistro(self):
        codigo = self.cleaned_data["codregistro"]
        if len(codigo) == 6:
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError("El codigo es incorrecto")
        else:
            raise forms.ValidationError("El codigo es incorrecto")
