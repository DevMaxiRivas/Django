from typing import Any
from django.shortcuts import render, redirect, get_object_or_404

# Autenticacion
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

from django.urls import reverse

# Vistas
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    TemplateView,
)


# # Grupos
from django.contrib.auth.models import Group

# # Formularios
from .forms import (
    DetailFoodOrderFormSet,
    PurchaseReceiptForm,
    TicketFormSet,
    TicketSalesForm,
    PassengerForm,
    RegisterForm,
)

# Modelos
from .models import Passenger, TicketSales, Ticket

# Base de Datos
from django.db import transaction

# Response
from django.http import JsonResponse

# Mails
from django.core.mail import send_mail

# Configuraciones para Mails
from django.conf import settings

# Listas
from django.views import generic


class HomeView(TemplateView):
    template_name = "home.html"

    # Funcion que determina el Grupo al que pertenece el usuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name

        context["group_name"] = group_name
        return context


# # REGISTRO DE USUARIOS
class RegisterView(View):
    # Cargamos la pagina con el fprmulario
    def get(self, request):
        data = {"form": RegisterForm()}
        return render(request, "registration/register.html", data)

    # Manejamos el formulario que se envia al servidor
    def post(self, request):
        user_creation_form = RegisterForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data["username"],
                password=user_creation_form.cleaned_data["password1"],
            )
            login(request, user)

            # Actualizar el campo created_by_admin del modelo Profile
            user.profile.created_by_admin = False
            user.profile.save()

            return redirect("home")
        data = {"form": user_creation_form}
        return render(request, "registration/register.html", data)


# Registros de Ventas
def purchase_success(request):
    return render(request, "purchase_success.html")


@require_http_methods(["GET", "POST"])
@transaction.atomic
def purchase_tickets(request):
    if request.method == "POST":
        msg = ""
        sales_form = TicketSalesForm(request.POST)
        formset = TicketFormSet(request.POST, prefix="tickets")

        if sales_form.is_valid() and formset.is_valid():
            all_passengers_exist = True
            all_passengers_no_deleted = False
            # print(formset)
            for form in formset:
                # print(type(form))
                if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                    # print(form.cleaned_data)
                    all_passengers_no_deleted = True
                    # print(all_passengers_no_deleted)
                    dni_or_passport = form.cleaned_data["dni_or_passport"]
                    passenger = Passenger.objects.filter(
                        dni_or_passport=dni_or_passport
                    ).first()
                    if not passenger:
                        all_passengers_exist = False
                        missing_passengers = dni_or_passport

            if not all_passengers_no_deleted:
                return JsonResponse(
                    {
                        "error": "All ticket forms must be filled out.",
                        "empty_form": True,
                    },
                    status=400,
                )

            if all_passengers_exist:
                sale = sales_form.save(commit=False)
                email = sales_form.cleaned_data.get("email")

                if request.user.is_authenticated:
                    sale.user = request.user

                sale.save()

                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                        # print(form.cleaned_data)
                        # print("Siguiente")
                        dni_or_passport = form.cleaned_data["dni_or_passport"]
                        passenger = Passenger.objects.filter(
                            dni_or_passport=dni_or_passport
                        ).first()
                        # print(passenger)
                        ticket = form.save(commit=False)
                        ticket.sale = sale
                        ticket.passenger = passenger
                        msg += "\n" + passenger.dni_or_passport
                        ticket.save()

                sale.update_total_price()

                if not request.user.is_authenticated and email:
                    send_mail(
                        "Your Tickets Purchased",
                        f"Here is the information about your ticket purchase. {msg}",
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )

                return JsonResponse(
                    {"success": True, "redirect_url": reverse("purchase_success")}
                )

            return JsonResponse(
                {
                    "error": "Some passengers are not loaded. Please provide missing details.",
                    "missing_passengers": missing_passengers,
                },
                status=400,
            )
        else:
            errors = {}
            if not sales_form.is_valid():
                errors.update(sales_form.errors)
            if not formset.is_valid():
                for i, form_errors in enumerate(formset.errors):
                    if form_errors:
                        errors[f"ticket_{i}"] = form_errors
            return JsonResponse({"errors": errors}, status=400)

    else:
        sales_form = TicketSalesForm()
        formset = TicketFormSet(prefix="tickets")

    context = {
        "sales_form": sales_form,
        "formset": formset,
        "empty_form": TicketFormSet(prefix="tickets").empty_form,
    }
    return render(request, "purchase_tickets.html", context)


def create_passenger(request):
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save()
            return JsonResponse({"success": True, "name": passenger.name})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        dni_or_passport = request.GET.get("dni_or_passport", "")
        form = PassengerForm(initial={"dni_or_passport": dni_or_passport})
    return render(request, "create_passenger.html", {"form": form})


def check_passenger(request):
    dni_or_passport = request.GET.get("dni_or_passport", None)
    if dni_or_passport:
        passenger = Passenger.objects.filter(dni_or_passport=dni_or_passport).first()
        if passenger:
            return JsonResponse({"exists": True, "name": passenger.name})
        else:
            return JsonResponse({"exists": False})
    return JsonResponse({"error": "No DNI/Passport provided"}, status=400)


# Ventas Comidas
# PROBAR HACER UNA COMPRA PARA VERIFICAR EL ERROR
@require_http_methods(["GET", "POST"])
@transaction.atomic
def purchase_food(request):
    if request.method == "POST":
        sales_form = PurchaseReceiptForm(request.POST)
        formset = DetailFoodOrderFormSet(request.POST, prefix="meals")

        if sales_form.is_valid() and formset.is_valid():
            all_foods_no_deleted = False
            # print(formset)
            for form in formset:
                # print(type(form))
                if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                    all_foods_no_deleted = True

            if not all_foods_no_deleted:
                return JsonResponse(
                    {
                        "error": "All foods forms must be filled out.",
                        "empty_form": True,
                    },
                    status=400,
                )

            dni_or_passport = sales_form.cleaned_data.get("dni_or_passport")
            if dni_or_passport:
                passenger = Passenger.objects.filter(
                    dni_or_passport=dni_or_passport
                ).first()

            if passenger:
                sale = sales_form.save(commit=False)
                sale.passenger = passenger
                sale.save()

                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                        # print(form.cleaned_data)
                        # print("Siguiente")
                        # print(passenger)
                        ticket = form.save(commit=False)
                        print(sale)
                        ticket.receipt = sale
                        ticket.save()

                sale.update_total_price()

                return JsonResponse(
                    {"success": True, "redirect_url": reverse("purchase_success")}
                )

            return JsonResponse(
                {
                    "error": "Passenger are not loaded. Please provide missing details.",
                    "no_exist_passenger": True,
                },
                status=400,
            )
        else:
            errors = {}
            if not sales_form.is_valid():
                errors.update(sales_form.errors)
            if not formset.is_valid():
                for i, form_errors in enumerate(formset.errors):
                    if form_errors:
                        errors[f"ticket_{i}"] = form_errors
            return JsonResponse({"errors": errors}, status=400)

    else:
        sales_form = PurchaseReceiptForm()
        formset = DetailFoodOrderFormSet(prefix="meals")

    context = {
        "sales_form": sales_form,
        "formset": formset,
        "empty_form": DetailFoodOrderFormSet(prefix="meals").empty_form,
    }
    return render(request, "purchase_tickets.html", context)


# LISTAS
def is_client(user):
    return user.groups.filter(name="clientes").exists()


def is_salesman(user):
    return user.groups.filter(name="vendedores").exists()


@login_required
@user_passes_test(is_client)
def client_purchases(request):
    sales = TicketSales.objects.filter(user=request.user)
    sales_with_urls = []
    for sale in sales:
        sale_detail_url = reverse("sale_detail", args=[sale.id])
        sales_with_urls.append(
            {
                "sale": sale,
                "detail_url": sale_detail_url,
            }
        )
    return render(
        request, "client_purchases.html", {"sales_with_urls": sales_with_urls}
    )


@login_required
@user_passes_test(is_client)
def sale_detail(request, sale_id):
    sale = TicketSales.objects.all(id=sale_id)
    tickets = (
        sale.tickets.all()
    )  # Utiliza el related_name 'tickets' para obtener todos los tickets asociados a esa venta
    return render(request, "sale_detail.html", {"sale": sale, "tickets": tickets})


@login_required
@user_passes_test(is_salesman)
def purchases(request):
    sales = TicketSales.objects.all()
    sales_with_urls = []
    for sale in sales:
        sale_detail_url = reverse("sale_details", args=[sale.id])
        sales_with_urls.append(
            {
                "sale": sale,
                "detail_url": sale_detail_url,
            }
        )
    return render(request, "purchases.html", {"sales_with_urls": sales_with_urls})


@login_required
@user_passes_test(is_salesman)
def sale_details(request, sale_id):
    sale = TicketSales.objects.get(id=sale_id)
    tickets = (
        sale.tickets.all()
    )  # Utiliza el related_name 'tickets' para obtener todos los tickets asociados a esa venta
    return render(request, "sale_detail.html", {"sale": sale, "tickets": tickets})
