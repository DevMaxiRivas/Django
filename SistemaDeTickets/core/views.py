# # PAGINA DE INICIO

from typing import Any
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

# # Autenticacion
from django.contrib.auth import authenticate, login

# # Vistas
from django.urls import reverse
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

# # Grupos
from django.contrib.auth.models import Group

# # Formularios
from .forms import RegisterForm, UserCreationForm
from django.views import View


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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TicketSales, Ticket, Passenger
from django.db import transaction
from .forms import TicketFormSet, TicketFormSetHelper
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from .forms import TicketSalesForm, TicketFormSet, PassengerForm
from django.http import JsonResponse


# @login_required
# @transaction.atomic
# def purchase_tickets(request):
#     if request.method == "POST":
#         print("POST data:", request.POST)
#         sales_form = TicketSalesForm(request.POST)
#         formset_prefix = "tickets"
#         formset = TicketFormSet(request.POST, prefix=formset_prefix)

#         if sales_form.is_valid():
#             sale = sales_form.save(commit=False)
#             sale.user = request.user
#             sale.save()
#             print("Sale created:", sale)

#             if formset.is_valid():
#                 tickets = formset.save(commit=False)
#                 print("Number of tickets:", len(tickets))
#                 for ticket in tickets:
#                     ticket.sale = sale
#                     ticket.save()
#                     print("Ticket saved:", ticket)
#                 formset.save_m2m()
#                 sale.update_total_price()
#                 return redirect("purchase_success")
#             else:
#                 print("Formset errors:", formset.errors)
#                 print("Non-form errors:", formset.non_form_errors())
#         else:
#             print("Sales form errors:", sales_form.errors)
#     else:
#         sales_form = TicketSalesForm()
#         formset_prefix = "tickets"
#         formset = TicketFormSet(prefix=formset_prefix)

#     context = {
#         "sales_form": sales_form,
#         "formset": formset,
#         "empty_form": TicketFormSet(prefix=formset_prefix).empty_form,
#     }
#     return render(request, "purchase_tickets.html", context)


def purchase_success(request):
    return render(request, "purchase_success.html")


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
@transaction.atomic
def purchase_tickets(request):
    if request.method == "POST":
        sales_form = TicketSalesForm(request.POST)
        formset = TicketFormSet(request.POST, prefix="tickets")
        if sales_form.is_valid() and formset.is_valid():
            # Verificar todos los pasajeros antes de guardar la venta
            all_passengers_exist = True
            for form in formset:
                if form.cleaned_data:
                    dni_or_passport = form.cleaned_data["dni_or_passport"]
                    passenger = Passenger.objects.filter(
                        dni_or_passport=dni_or_passport
                    ).first()
                    if not passenger:
                        all_passengers_exist = False
                        return JsonResponse(
                            {
                                "error": f"Passenger with DNI/Passport {dni_or_passport} does not exist.",
                                "dni_or_passport": dni_or_passport,
                            },
                            status=400,
                        )

            # Si todos los pasajeros existen, guardar la venta y los tickets
            if all_passengers_exist:
                sale = sales_form.save(commit=False)
                sale.user = request.user
                sale.save()

                for form in formset:
                    if form.cleaned_data:
                        dni_or_passport = form.cleaned_data["dni_or_passport"]
                        passenger = Passenger.objects.get(
                            dni_or_passport=dni_or_passport
                        )
                        ticket = form.save(commit=False)
                        ticket.sale = sale
                        ticket.passenger = passenger
                        ticket.save()

                sale.update_total_price()
                return JsonResponse(
                    {"success": True, "redirect_url": reverse("purchase_success")}
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
