from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("index/", views.index, name="dashboard-index"),
    path("products/", views.products, name="dashboard-products"),
    path(
        "products/delete/<int:pk>/",
        views.product_delete,
        name="dashboard-products-delete",
    ),
    path("products/edit/<int:pk>/", views.product_edit, name="dashboard-products-edit"),
    path(
        "products/detail/<int:pk>/",
        views.product_detail,
        name="dashboard-products-detail",
    ),
    path("purchases/", views.purchases, name="dashboard-purchases"),
    path("sale/<int:sale_id>/", sale_detail, name="dashboard-sale_detail"),
    path("meals/", views.meals, name="dashboard-meals"),
    path("meals/edit/<int:pk>/", views.meal_edit, name="dashboard-meal-edit"),
    path(
        "meals/delete/<int:pk>/",
        views.meal_delete,
        name="dashboard-meal-delete",
    ),
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
    path("customers/", views.customers, name="dashboard-customers"),
    path(
        "customers/detail/<int:pk>/",
        views.customer_detail,
        name="dashboard-customer-detail",
    ),
    path("order/", views.order, name="dashboard-order"),
    # VENTA DE TICKETS
    path("purchase-tickets/", views.purchase_tickets, name="purchase_tickets"),
    # Pagos
    path("payment_success/", views.payment_success, name="payment_success"),
    path("payment_failed/", views.payment_failed, name="payment_failed"),
    path("payment_pending/", views.payment_pending, name="payment_pending"),
    # path("payment_detail/<int:sale_id>", views.payment_detail, name="payment_detail"),
    # Pasajeros
    path("create_passenger/", views.create_passenger, name="create_passenger"),
]
