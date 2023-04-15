from django.urls import path
from .import views

app_name = "users_app"
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="user-register" ),
    path('login/', views.LoginUser.as_view(), name="user-login" ),
    path('logout/', views.LogoutUser.as_view(), name="user-logout" ),
    path('update/', views.updatePassword.as_view(), name="user-update" ),
    path('verification/<pk>/', views.CodeVerificacionEmailView.as_view(), name="user-verification" ),
]