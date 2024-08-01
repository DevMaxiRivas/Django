from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="home"),
    # CUSTOMERS
    path("customers_index/", views.index_customer, name="dashboard-customers-index"),
    path("customer_tickets/", views.customer_tickets, name="customer_tickets"),
    path(
        "ticket-data/<int:pk>/",
        views.ticket_data,
        name="ticket_data",
    ),
    # EMPLOYEES
    path("employee_index/", views.index_employee, name="dashboard-employee-index"),
    # PRODUCTS
    path("products/", views.products, name="dashboard-products"),
    path(
        "products/delete/<int:pk>/",
        views.product_delete,
        name="dashboard-product-delete",
    ),
    path("products/edit/<int:pk>/", views.product_edit, name="dashboard-product-edit"),
    path(
        "products/detail/<int:pk>/",
        views.product_detail,
        name="dashboard-products-detail",
    ),
    # VENTAS
    path("purchases/", views.purchases, name="dashboard-purchases"),
    path("sale/<int:sale_id>/", sale_detail, name="dashboard-sale_detail"),
    path(
        "purchase_detail/<int:sale_id>",
        views.purchase_detail,
        name="purchase_detail",
    ),
    # Recibos
    path("receipts/", views.receipts, name="dashboard-receipts"),
    path(
        "receipt_detail/<int:sale_id>/", receipt_detail, name="dashboard-receipt_detail"
    ),
    path(
        "receipt_payment/<int:sale_id>",
        views.receipt_payment,
        name="dashboard-receipt_payment",
    ),
    # PLATOS
    path("meals/", views.meals, name="dashboard-meals"),
    path("meals/edit/<int:pk>/", views.meal_edit, name="dashboard-meal-edit"),
    path(
        "meals/delete/<int:pk>/",
        views.meal_delete,
        name="dashboard-meal-delete",
    ),
    # ASIENTOS
    path("seats/", views.seats, name="dashboard-seats"),
    path(
        "seats/edit/<int:pk>/",
        views.seat_edit,
        name="dashboard-seat-edit",
    ),
    path(
        "seats/delete/<int:pk>/",
        views.seat_delete,
        name="dashboard-seat-delete",
    ),
    # COLECTIVOS
    path("buses/", views.buses, name="dashboard-buses"),
    path(
        "buses/edit/<int:pk>/",
        views.bus_edit,
        name="dashboard-bus-edit",
    ),
    path(
        "buses/delete/<int:pk>/",
        views.bus_delete,
        name="dashboard-bus-delete",
    ),
    # TRENES
    path("trains/", views.trains, name="dashboard-trains"),
    path(
        "trains/edit/<int:pk>/",
        views.train_edit,
        name="dashboard-train-edit",
    ),
    path(
        "trains/delete/<int:pk>/",
        views.train_delete,
        name="dashboard-train-delete",
    ),
    # TIPOS DE RECORRIDO
    path("types_journey/", views.types_journey, name="dashboard-types_journey"),
    path(
        "types_journey/edit/<int:pk>/",
        views.type_journey_edit,
        name="dashboard-type_journey-edit",
    ),
    path(
        "types_journey/delete/<int:pk>/",
        views.type_journey_delete,
        name="dashboard-type_journey-delete",
    ),
    # ETAPAS DE RECORRIDOS
    path("journey_stages/", views.journey_stages, name="dashboard-journey_stages"),
    path(
        "journey_stages/edit/<int:pk>/",
        views.journey_stage_edit,
        name="dashboard-journey_stage-edit",
    ),
    path(
        "journey_stages/delete/<int:pk>/",
        views.journey_stage_delete,
        name="dashboard-journey_stage-delete",
    ),
    # CRONOGRAMAS DE RECORRIDOS
    path(
        "journey_schedules/",
        views.journey_schedules,
        name="dashboard-journey_schedules",
    ),
    path(
        "journey_schedules/edit/<int:pk>/",
        views.journey_schedule_edit,
        name="dashboard-journey_schedule-edit",
    ),
    path(
        "journey_schedules/delete/<int:pk>/",
        views.journey_schedule_delete,
        name="dashboard-journey_schedule-delete",
    ),
    # PARADAS
    path("stops/", views.stops, name="dashboard-stops"),
    path(
        "stops/edit/<int:pk>/",
        views.stop_edit,
        name="dashboard-stop-edit",
    ),
    path(
        "stops/delete/<int:pk>/",
        views.stop_delete,
        name="dashboard-stop-delete",
    ),
    # CATEGORIAS DE PLATOS
    path("meal_categories/", views.meal_categories, name="dashboard-meal_categories"),
    path(
        "meal_categories/edit/<int:pk>/",
        views.meal_category_edit,
        name="dashboard-meal_category-edit",
    ),
    path(
        "meal_categories/delete/<int:pk>/",
        views.meal_category_delete,
        name="dashboard-meal_category-delete",
    ),
    # CATEGORIAS DE PRODUCTOS
    path(
        "product_categories/",
        views.product_categories,
        name="dashboard-product_categories",
    ),
    path(
        "product_categories/edit/<int:pk>/",
        views.product_category_edit,
        name="dashboard-product_category-edit",
    ),
    path(
        "product_categories/delete/<int:pk>/",
        views.product_category_delete,
        name="dashboard-product_category-delete",
    ),
    # CATEGORIAS DE ASIENTOS
    path("seat_categories/", views.seat_categories, name="dashboard-seat_categories"),
    path(
        "seat_categories/edit/<int:pk>/",
        views.seat_category_edit,
        name="dashboard-seat_category-edit",
    ),
    path(
        "seat_categories/delete/<int:pk>/",
        views.seat_category_delete,
        name="dashboard-seat_category-delete",
    ),
    # DASHBOARD DE USUARIOS
    path("customers/", views.customers, name="dashboard-customers"),
    path("employees/", views.employees, name="dashboard-employees"),
    path("admins/", views.admins, name="dashboard-admins"),
    path(
        "user_detail/detail/<int:pk>/",
        views.user_detail,
        name="dashboard-user-detail",
    ),
    path("order/", views.order, name="dashboard-order"),
    # VENTA DE TICKETS
    path("purchase-tickets/", views.purchase_tickets, name="purchase_tickets"),
    # Pagos
    path("payments/", views.payments, name="dashboard-payments"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("payment_failed/", views.payment_failed, name="payment_failed"),
    path("payment_pending/", views.payment_pending, name="payment_pending"),
    # Pasajeros
    path("create_passenger/", views.create_passenger, name="create_passenger"),
    path("finances/", views.finances, name="dashboard-finances"),
    path("supplies/", views.supplies, name="dashboard-supplies"),
    path("journeys/", views.journeys, name="dashboard-journeys"),
    path("transports/", views.transports, name="dashboard-transports"),
    path("planning/", views.planning, name="dashboard-planning"),
    path("users/", views.users, name="dashboard-users"),
    path("prueba/", views.prueba, name="prueba"),
    # VENTAS DE PRODUCTOS
    path("product_sales/", views.product_sales, name="dashboard-product_sales"),
    # APIS
    path(
        "api/product_categories/",
        views.api_product_categories,
        name="api_product_categories",
    ),
    path(
        "api/products_per_category/",
        views.api_products_per_category,
        name="api_products_per_category",
    ),
]
