from django.views.generic import FormView , View
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as loginUser, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationCodeEmail
from .models import User
from .functions import code_generator

class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"
    
    #Definiendo oroceso de guardar para guardar informacion
    def form_valid(self, form):
        #generando el codigo de vcerificacion
        codigo = code_generator()
        
        usuario = User.objects.create_user(
           #Parametros creando usuario
           form.cleaned_data["username"],
           form.cleaned_data["email"],
           form.cleaned_data["password1"],
           nombres = form.cleaned_data["nombres"],
           apellidos = form.cleaned_data["apellidos"],
           genero = form.cleaned_data["genero"],
           codregistro = codigo
        )
        
        #enviar el codigo por email
        asunto = "Confirmacion de email"
        mensaje = "Codigo de verificacion: "+ codigo
        email_remitente = "jamaicabarbershop1@gmail.com"
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data["email"]])
        #redirigir a pantalla de validacion
        return HttpResponseRedirect(
            reverse_lazy(
                "users_app:user-verification",
                kwargs = {"pk" : usuario.id}
            )
            
        )
        
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
        
class updatePassword(LoginRequiredMixin, FormView):
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("users_app:user-login")
    login_url = reverse_lazy("users_app:user-login")
    
    #Definiendo oroceso de guardar para guardar informacion
    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data["password1"]
        )
        
        if user:
            new_password = form.cleaned_data["password2"]
            usuario.set_password(new_password)
            #usuario.save()
            
        logout(self.request)
        return super(updatePassword, self).form_valid(form)
    
class CodeVerificacionEmailView(FormView):
    template_name = "users/verification.html"
    form_class = VerificationCodeEmail
    success_url = reverse_lazy("users_app:user-login")
    
    def get_form_kwargs(self):
        kwargs = super(CodeVerificacionEmailView, self).get_form_kwargs()
        kwargs.update(
            {"pk": self.kwargs["pk"],}
        )
        return kwargs
    
    def form_valid(self, form):
        #recurenado id del usuario y actualizando el usuarrio
        User.objects.filter(
            id = self.kwargs["pk"]
        ).update(
            is_active = True
        )
        return super(CodeVerificacionEmailView, self).form_valid(form)