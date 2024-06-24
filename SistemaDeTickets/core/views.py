# # PAGINA DE INICIO

from typing import Any
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

# # Autenticacion
from django.contrib.auth import authenticate, login

# # Vistas
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
from .models import TicketSales, Ticket
from django.db import transaction
from .forms import TicketFormSet, TicketFormSetHelper
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from .forms import TicketSalesForm, TicketFormSet


@login_required
@transaction.atomic
def purchase_tickets(request):
    if request.method == "POST":
        print("POST data:", request.POST)
        sales_form = TicketSalesForm(request.POST)
        if sales_form.is_valid():
            sale = sales_form.save(commit=False)
            sale.user = request.user
            sale.save()
            print("Sale created:", sale)

            formset = TicketFormSet(request.POST, instance=sale)
            print("Formset is bound:", formset.is_bound)
            print("Formset is valid:", formset.is_valid())
            if formset.is_valid():
                tickets = formset.save(commit=False)
                print("Number of tickets:", len(tickets))
                for ticket in tickets:
                    ticket.sale = sale
                    ticket.save()
                    print("Ticket saved:", ticket)
                formset.save_m2m()
                sale.update_total_price()
                return redirect("purchase_success")
            else:
                print("Formset errors:", formset.errors)
                print("Non-form errors:", formset.non_form_errors())
        else:
            print("Sales form errors:", sales_form.errors)
    else:
        sales_form = TicketSalesForm()
        formset = TicketFormSet(instance=TicketSales())

    context = {
        "sales_form": sales_form,
        "formset": formset,
        "empty_form": TicketFormSet(instance=TicketSales()).empty_form,
    }
    return render(request, "purchase_tickets.html", context)


def purchase_success(request):
    return render(request, "purchase_success.html")
