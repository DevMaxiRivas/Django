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
    # Pagos
    path("payment_success/", views.payment_success, name="payment_success"),
    path("payment_failed/", views.payment_failed, name="payment_failed"),
    path("payment_pending/", views.payment_pending, name="payment_pending"),
    # COMPROBACIÓN DE PASAJEROS
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
    # Vemtas de boletos
    path("purchases/", purchases, name="purchases"),
    # Compra de productos
    path("receipts/", receipts, name="receipts"),
    path("receipt-details/<int:receipt_id>/", receipt_details, name="receipt_details"),
    # Recorridos y Cronogramas
    path("journeys/", journeys, name="journeys"),
    path("journey_schedules/", journey_schedules, name="journey_schedules"),
    path(
        "journey_schedules/new/",
        views.journey_schedule_new,
        name="journey_schedule_new",
    ),
    path(
        "journey_schedules/update/<pk>",
        views.journey_schedule_update,
        name="journey_schedule_update",
    ),
    path(
        "journey_schedules/delete/<pk>",
        views.journey_schedule_delete,
        name="journey_schedule_delete",
    ),
    # Merchaderias
    path("merchandises/", merchandises, name="merchandises"),
    path(
        "merchandises/new/",
        views.merchandise_new,
        name="merchandise_new",
    ),
    path(
        "merchandises/update/<pk>",
        views.merchandise_update,
        name="merchandise_update",
    ),
    path(
        "merchandises/delete/<pk>",
        views.merchandise_delete,
        name="merchandise_delete",
    ),
    # Platillos
    path("meals/", meals, name="meals"),
    path(
        "meals/new/",
        views.meal_new,
        name="meal_new",
    ),
    path(
        "meals/update/<pk>",
        views.meal_update,
        name="meal_update",
    ),
    path(
        "meals/delete/<pk>",
        views.meal_delete,
        name="meal_delete",
    ),
]
