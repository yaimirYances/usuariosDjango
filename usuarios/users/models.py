from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    
    GENERO = (
        ("M", "Masculino"),
        ("F", "Femenino"),
    )
    
    #Variables de autenticacion USERNAME_FIELD
    #utilizado como predetrminado para iniciar sesion
    USERNAME_FIELD = "username"
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=50, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO, blank=True)
    codregistro =models.CharField(max_length=6, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    objects = UserManager()
    
    #Requerimientos para la creacion de super usuarios
    REQUIRED_FIELDS = ["email"]

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres+" "+self.apellidos
    
    def __str__(self):
        if self.is_active:
            estado = "Activo"
        else:
            estado = "Desativado"
        return self.username+" "+estado
    