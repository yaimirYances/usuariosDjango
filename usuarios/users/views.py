from django.views.generic import FormView , View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as loginUser, logout
from django.http import HttpResponseRedirect

from .forms import UserRegisterForm, LoginForm
from .models import User

class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"
    
    #Definiendo oroceso de guardar para guardar informacion
    def form_valid(self, form):
        User.objects.create_user(
           #Parametros
           form.cleaned_data["username"],
           form.cleaned_data["email"],
           form.cleaned_data["password1"],
           nombres = form.cleaned_data["nombres"],
           apellidos = form.cleaned_data["apellidos"],
           genero = form.cleaned_data["genero"]
        )
        
        return super(UserRegisterView, self).form_valid(form)
        
class LoginUser(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home_app:panel")
    
    #Definiendo oroceso de guardar para guardar informacion
    def form_valid(self, form):
        #recuperando usuario autenticado 
        user = authenticate(
            username = form.cleaned_data["username"],
            password = form.cleaned_data["password"],
        )
        #Haciendo login del usuario
        loginUser(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutUser(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse_lazy("users_app:user-login")
        )