from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="home"),
    # CUSTOMERS
    path("customers_index/", views.index_customer, name="dashboard-customers-index"),
    path("customer_tickets/", views.customer_tickets, name="customer_tickets"),
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
    # PLATOS
    path("meals/", views.meals, name="dashboard-meals"),
    path("meals/edit/<int:pk>/", views.meal_edit, name="dashboard-meal-edit"),
    path(
        "meals/delete/<int:pk>/",
        views.meal_delete,
        name="dashboard-meal-delete",
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
    path("payment_success/", views.payment_success, name="payment_success"),
    path("payment_failed/", views.payment_failed, name="payment_failed"),
    path("payment_pending/", views.payment_pending, name="payment_pending"),
    # Pasajeros
    path("create_passenger/", views.create_passenger, name="create_passenger"),
    path("finances/", views.finances, name="dashboard-finances"),
    path("supplies/", views.supplies, name="dashboard-supplies"),
    path("users/", views.users, name="dashboard-users"),
]
