# Requerst
import datetime
from django.shortcuts import render, redirect, get_object_or_404

# Modelos de Sistema
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Vistas
from django.views.generic import TemplateView

# Response
from django.http import JsonResponse

# # Formularios
from .forms import *

# Modelos
from .models import *

# Mensajes
from django.contrib import messages

# Decoradores
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import auth_users, allowed_users
from django.views.decorators.http import require_http_methods

from django.urls import reverse

# Base de Datos
from django.db import transaction

# Mails
from django.core.mail import EmailMessage

# Generación de PDF's
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from io import BytesIO

# Ruta static
from django.templatetags.static import static

# Acciones del sistema
import os

# Configuraciones para Mails
from django.conf import settings

# Listas
from django.views import generic

# Pagos
import mercadopago


# Traducciones
from django.utils.translation import gettext as _

# Envio de Emails
from .sendEmails import send_pdf_via_email


# Control de Acceso
def is_client(user):
    return user.groups.filter(name="Customers").exists()


def is_salesman(user):
    return user.groups.filter(name="Employees").exists()


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_employee(user):
    return is_admin(user) or is_salesman(user)


# Obtener rol del usuario
def get_user_group(user):
    if user.is_authenticated:
        group = Group.objects.filter(user=user).first()
        return group.name
    return None


@login_required(login_url="user-login")
def index_customer(request):

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect("home")
    else:
        form = OrderForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/customer_index.html", context)


@login_required
@user_passes_test(is_client)
def customer_tickets(request):
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
        request,
        "public/client_purchases.html",
        {
            "user_group": get_user_group(request.user),
            "sales_with_urls": sales_with_urls,
        },
    )


def index(request):
    if not request.user.is_authenticated or is_client(request.user):
        return render(
            request,
            "public/home.html",
            {
                "user_group": get_user_group(request.user),
            },
        )

    if is_employee(request.user):
        return redirect("dashboard-employee-index")


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def index_employee(request):
    order = Order.objects.all()
    product = Product.objects.all()
    months = [
        ("January"),
        ("February"),
        ("March"),
        ("April"),
        ("May"),
        ("June"),
        ("July"),
        ("August"),
        ("September"),
        ("October"),
        ("November"),
        ("December"),
    ]

    query = Ticket.revenue_by_seat_category()

    revenue_by_seat_category = []

    for rev in query:
        revenue_by_seat_category.append(
            [str(rev["seat__category__type"]), float(rev["total_ingresos"])]
        )

    query2 = Journey.passengers_for_journey()
    passengers_for_journey = []

    for rev in query2:
        passengers_for_journey.append([str(rev["type"]), int(rev["total_passengers"])])

    context = {
        "order": order,
        "product": product,
        "months": months[: datetime.datetime.now().month],
        "revenue_by_seat_category": revenue_by_seat_category,
        "passengers_for_journey": passengers_for_journey,
    }
    return render(request, "dashboard/index.html", context)


@login_required(login_url="user-login")
def product_categories(request):
    categories = ProductCategory.objects.all()

    if request.method == "POST":
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            category_name = form.cleaned_data.get("name")
            messages.success(request, f"{category_name} has been added")
            return redirect("dashboard-product_categories")
    else:
        form = ProductCategoryForm()
    context = {
        "categories": categories,
        "form": form,
    }
    return render(request, "dashboard/product_categories.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def product_category_edit(request, pk):
    item = ProductCategory.objects.get(id=pk)
    if request.method == "POST":
        form = ProductCategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-product_categories")
    else:
        form = ProductCategoryForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def product_category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()

    return redirect("dashboard-product_categories")


@login_required(login_url="user-login")
def products(request):
    product = Product.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get("name")
            messages.success(request, f"{product_name} has been added")
            return redirect("dashboard-products")
    else:
        form = ProductForm()
    context = {
        "product": product,
        "form": form,
    }
    return render(request, "dashboard/products.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def product_edit(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-products")
    else:
        form = ProductForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()

    return redirect("dashboard-products")


@login_required(login_url="user-login")
def product_detail(request, pk):
    context = {}
    return render(request, "dashboard/products_detail.html", context)


@login_required(login_url="user-login")
def meal_categories(request):
    categories = MealCategory.objects.all()

    if request.method == "POST":
        form = MealCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            category_name = form.cleaned_data.get("name")
            messages.success(request, f"{category_name} has been added")
            return redirect("dashboard-meal_categories")
    else:
        form = MealCategoryForm()
    context = {
        "categories": categories,
        "form": form,
    }
    return render(request, "dashboard/meal_categories.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def meal_category_edit(request, pk):
    item = MealCategory.objects.get(id=pk)
    if request.method == "POST":
        form = MealCategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-meal_categories")
    else:
        form = MealCategoryForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def meal_category_delete(request, pk):
    category = get_object_or_404(MealCategory, pk=pk)
    category.delete()

    return redirect("dashboard-meal_categories")


@login_required(login_url="user-login")
def meals(request):
    meals = Meal.objects.all()

    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            meal_name = form.cleaned_data.get("name")
            messages.success(request, f"{meal_name} has been added")
            return redirect("dashboard-meals")
    else:
        form = MealForm()
    context = {
        "meals": meals,
        "form": form,
    }
    return render(request, "dashboard/meals.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def meal_edit(request, pk):
    item = Meal.objects.get(id=pk)
    if request.method == "POST":
        form = MealForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-meals")
    else:
        form = MealForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    meal.delete()

    return redirect("dashboard-meals")


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def customers(request):

    users = User.objects.filter(groups=Group.objects.get(name="Customers"))
    context = {
        "users": users,
    }

    return render(request, "dashboard/customers.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def employees(request):

    users = User.objects.filter(groups=Group.objects.get(name="Employees"))
    context = {
        "users": users,
    }

    return render(request, "dashboard/employees.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def admins(request):

    users = User.objects.filter(groups=Group.objects.get(name="Admin"))
    context = {
        "users": users,
    }

    return render(request, "dashboard/employees.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def purchases(request):
    sales = TicketSales.objects.all()
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/purchases.html", context)


@login_required(login_url="user-login")
@allowed_users(allowed_roles=["Admin"])
def sale_detail(request, sale_id):
    sale = TicketSales.objects.get(id=sale_id)
    tickets = (
        sale.tickets.all()
    )  # Utiliza el related_name 'tickets' para obtener todos los tickets asociados a esa venta
    return render(
        request, "dashboard/sale_detail.html", {"sale": sale, "tickets": tickets}
    )


@login_required
@user_passes_test(is_employee)
def purchase_detail(request, sale_id):
    if TicketSales.objects.get(id=sale_id).payment:
        return render(
            request,
            "dashboard/purchase_detail.html",
            {"payment": TicketSales.objects.get(id=sale_id).payment},
        )
    return render(request, "dashboard/purchase_detail.html", {})


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def user_detail(request, pk):

    user = User.objects.get(id=pk)

    context = {
        "user": user,
    }
    return render(request, "dashboard/user_detail.html", context)


@login_required(login_url="user-login")
def order(request):
    order = Order.objects.all()

    context = {
        "order": order,
    }
    return render(request, "dashboard/order.html", context)


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

                # Crear una instancia de Mercado Pago
                mp = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

                # Crear una preferencia de pago
                preference_data = {
                    "items": [
                        {
                            "title": "Tickets",
                            "quantity": 1,
                            "currency_id": "ARS",
                            "unit_price": float(sale.price),
                        }
                    ],
                    "back_urls": {
                        "success": request.build_absolute_uri(
                            reverse("payment_success")
                        ),
                        "failure": request.build_absolute_uri(
                            reverse("payment_pending")
                        ),
                        "pending": request.build_absolute_uri(
                            reverse("payment_pending")
                        ),
                    },
                    "auto_return": "approved",
                    "payment_methods": {
                        "excluded_payment_types": [{"id": "ticket"}],
                        "installments": 1,
                    },
                    "external_reference": str(sale.id),
                }
                preference_response = mp.preference().create(preference_data)
                preference = preference_response["response"]

                return JsonResponse(
                    {"success": True, "init_point": preference["sandbox_init_point"]}
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

    if request.user.is_authenticated:
        context = {
            "user_group": get_user_group(request.user),
            "sales_form": sales_form,
            "formset": formset,
            "empty_form": TicketFormSet(prefix="tickets").empty_form,
        }
    else:
        context = {
            "sales_form": sales_form,
            "formset": formset,
            "empty_form": TicketFormSet(prefix="tickets").empty_form,
        }
    return render(request, "public/purchase_tickets.html", context)


def generate_pdf_receipt(sale):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Estilo de título
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1  # Centrar
    # Agregar imagen
    # Ruta de la imagen
    image_path = os.path.join(
        settings.BASE_DIR, "static", "img", "TrenALasNubesLogo.png"
    )
    elements.append(Image(image_path, width=130, height=58))

    # Título del documento
    elements.append(Paragraph("Comprobante", title_style))

    # Número de comprobante
    elements.append(
        Paragraph(
            f"Nro. Comprobante: {sale.payment.payment_id}",
            title_style,
        )
    )

    # Obtenemos todos los tickets de la venta
    tickets = sale.tickets.all()

    # Datos del ticket en formato de tabla
    data = [
        [
            _("DNI/Passport"),
            _("Name"),
            _("Schedule"),
            _("Train Seat"),
            _("Price"),
        ],
    ]

    for ticket in tickets:
        data.append(
            [
                ticket.passenger.dni_or_passport,
                ticket.passenger.name,
                ticket.schedule,
                ticket.seat,
                "${:.2f}".format(ticket.price),
            ]
        )
    data.append(["", "", "", "Total", "${:.2f}".format(sale.price)])
    # Tabla de detalles
    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)
    return buffer


def send_email(tickets, email):
    send_pdf_via_email(tickets, email)


def payment_success(request):
    payment_id = request.GET.get("payment_id")
    payment_type = request.GET.get("payment_type")
    payment_status = request.GET.get("status")
    sale_id = request.GET.get(
        "external_reference"
    )  # Se aume que se envia el id de la venta por "external_reference"
    sale = TicketSales.objects.get(id=sale_id)
    tickets = Ticket.objects.filter(sale=sale)

    if request.user.is_authenticated:
        email = sale.user.email
    else:
        email = sale.email

    if payment_id and payment_type and sale_id:
        sale = get_object_or_404(TicketSales, id=sale_id)
        payment = Payments.objects.create(
            payment_id=payment_id,
            payment_type=payment_type,
            payment_status=payment_status,
        )
        sale.payment = payment
        sale.save()
    if email:
        send_email(tickets, email)

    return render(request, "public/payment_success.html")


def payment_failed(request):
    sale_id = request.GET.get("external_reference")
    TicketSales.delete(TicketSales.objects.get(id=sale_id))
    return render(request, "public/payment_failed.html")


def payment_pending(request):
    sale = TicketSales.objects.get(id=11)
    tickets = Ticket.objects.filter(sale=sale)
    send_pdf_via_email(tickets, str(sale.email))
    # sale_id = request.GET.get("external_reference")
    # TicketSales.delete(TicketSales.objects.get(id=sale_id))s
    return render(request, "public/payment_pending.html")


def create_passenger(request):
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            if not Passenger.objects.filter(
                dni_or_passport=form.cleaned_data["dni_or_passport"]
            ).exists():
                form.save()
            else:
                Passenger.objects.filter(
                    dni_or_passport=form.cleaned_data["dni_or_passport"]
                ).update(**form.cleaned_data)
            name = form.cleaned_data["name"]
            return JsonResponse({"success": True, "name": name})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        dni_or_passport = request.GET.get("dni_or_passport", "")
        if Passenger.objects.filter(dni_or_passport=dni_or_passport).exists():
            passenger = Passenger.objects.get(dni_or_passport=dni_or_passport)
            form = PassengerForm(
                initial={
                    "name": passenger.name,
                    "dni_or_passport": dni_or_passport,
                    "origin_country": passenger.origin_country,
                    "emergency_telephone": passenger.emergency_telephone,
                    "date_of_birth": passenger.date_of_birth,
                    "gender": passenger.gender,
                }
            )
        else:
            form = PassengerForm(initial={"dni_or_passport": dni_or_passport})
    return render(request, "public/create_passenger.html", {"form": form})


@login_required
@user_passes_test(is_employee)
def finances(request):
    context = {
        "product": Product.objects.all(),
        "order": Order.objects.all(),
    }
    return render(request, "dashboard/finances.html", context)


@login_required
@user_passes_test(is_employee)
def supplies(request):
    context = {
        "product": Product.objects.all(),
        "order": Order.objects.all(),
    }
    return render(request, "dashboard/supplies.html", context)


@login_required
@user_passes_test(is_employee)
def users(request):
    context = {
        "product": Product.objects.all(),
        "order": Order.objects.all(),
    }
    return render(request, "dashboard/users.html", context)


def ticket_data(request, pk):
    if Ticket.objects.filter(id=pk).exists():
        ticket = Ticket.objects.get(id=pk)
        data = ticket.getDataPublic()
        return render(request, "public/ticket_data.html", {"data": data})
    return render(request, "public/ticket_data.html")
