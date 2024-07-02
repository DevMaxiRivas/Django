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
    path("get_passenger_info/", get_passenger_info, name="get_passenger_info"),
    # VENTAS DE COMIDAS
    path("purchase-foods/", views.purchase_food, name="purchase_foods"),
    path(
        "purchase-merchandise/", views.purchase_merchandise, name="purchase_merchandise"
    ),
    # Listas
    # Clientes
    path("my-purchases/", client_purchases, name="client_purchases"),
    path("sale/<int:sale_id>/", sale_detail, name="sale_detail"),
    # Vendedores
    path("sales/<int:sale_id>/", sale_details, name="sale_details"),
    # Administradores
    path("purchases/", purchases, name="purchases"),
    path("receipts/", receipts, name="receipts"),
    path("receipt-details/<int:receipt_id>/", receipt_details, name="receipt_details"),
    path("journeys/", journeys, name="journeys"),
    path("journey_schedules/", journey_schedules, name="journey_schedules"),
]
