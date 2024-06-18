from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # PAGINA DE INICIO
    path("", HomeView.as_view(), name="home"),
    # # PAGINAS DE LOGIN Y REGISTRO
    path("register/", RegisterView.as_view(), name="register"),
]
