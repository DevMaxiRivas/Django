from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # PAGINA DE INICIO
    path("", HomeView.as_view(), name="home"),
    # # PAGINAS DE LOGIN Y REGISTRO
    path("register/", RegisterView.as_view(), name="register"),
    # VENTA DE TICKETS
    path("purchase-tickets/", views.purchase_tickets, name="purchase_tickets"),
    path("purchase-success/", views.purchase_success, name="purchase_success"),
    path("check_passenger/", views.check_passenger, name="check_passenger"),
    path("create_passenger/", views.create_passenger, name="create_passenger"),
    # Listas
    path("my-purchases/", client_purchases, name="client_purchases"),
    path("sale/<int:sale_id>/", sale_detail, name="sale_detail"),
]
