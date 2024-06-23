from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # PAGINA DE INICIO
    path("", HomeView.as_view(), name="home"),
    # # PAGINAS DE LOGIN Y REGISTRO
    path("register/", RegisterView.as_view(), name="register"),
    path("purchase-tickets/", views.purchase_tickets, name="purchase_tickets"),
    path("purchase-success/", views.purchase_success, name="purchase_success"),
]
