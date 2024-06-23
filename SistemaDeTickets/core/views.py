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


@login_required  # Unicamente los usuarios logueados pueden reservar boletos
@transaction.atomic  # Si la funcion devuelve un error, se elimina la venta se hace un rolback en la base de datos
def purchase_tickets(request):
    if request.method == "POST":  # Si se envio el formulario
        # queryset=Ticket.objects.none() indica que estamos creando nuevos tickets, no editando existente
        formset = TicketFormSet(request.POST, queryset=Ticket.objects.none())
        if formset.is_valid():
            try:
                with transaction.atomic():
                    # Crea una nueva venta (TicketSales) asociada al usuario actual.
                    sale = TicketSales.objects.create(user=request.user)

                    total_price = 0
                    # Itera sobre cada formulario en el formset. form.cleaned_data contiene los datos validados del formulario.
                    for form in formset:
                        if form.cleaned_data and not form.cleaned_data.get(
                            "DELETE", False
                        ):
                            # Crea un nuevo objeto Ticket pero no lo guarda en la base de datos aún (commit=False).
                            ticket = form.save(commit=False)
                            ticket.sale = sale
                            ticket.price = ticket.seat.category.price

                            # Verifica que el asiento no este reservado.
                            if ticket.seat.is_reserved:
                                raise ValidationError(
                                    f"Seat {ticket.seat} is already reserved."
                                )
                            # Guarda el ticket en la base de datos
                            ticket.save()
                            ticket.reserveSeat()
                            total_price += ticket.price

                    # Actualiza el precio total de la venta y la guarda en la base de datos.
                    sale.price = total_price
                    sale.save()

                # Si todo ha ido bien, redirige al usuario a la página de éxito de la compra.
                return redirect("purchase_success")
            except ValidationError as e:
                # Si se produce un error de validación, elimina la venta creada y añade el error al formset para mostrarlo al usuario.
                sale.delete()
                formset.add_error(None, str(e))
    else:
        # Si la solicitud no es POST crea un formset vacío.
        formset = TicketFormSet(queryset=Ticket.objects.none())
    # Crea un helper de crispy forms para el formset
    helper = TicketFormSetHelper()
    return render(
        request, "purchase_tickets.html", {"formset": formset, "helper": helper}
    )


def purchase_success(request):
    return render(request, "purchase_success.html")
