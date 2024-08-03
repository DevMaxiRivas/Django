# Requerst
# import datetime
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

# Archivos JSON
import json

# Fechas
from datetime import datetime


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


@login_required
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

    # query = Ticket.revenue_by_journey_price()

    # revenue_by_journey_price = []

    # for rev in query:
    #     revenue_by_journey_price.append(
    #         [str(rev["seat__category__type"]), float(rev["total_ingresos"])]
    #     )

    query2 = Journey.passengers_for_journey()
    passengers_for_journey = []

    for rev in query2:
        passengers_for_journey.append([str(rev["type"]), int(rev["total_passengers"])])

    context = {
        "order": order,
        "product": product,
        "months": months[: datetime.now().month],
        # "revenue_by_journey_price": revenue_by_journey_price,
        "passengers_for_journey": passengers_for_journey,
    }
    return render(request, "dashboard/index.html", context)


@login_required
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
def product_category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()

    return redirect("dashboard-product_categories")


@login_required
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()

    return redirect("dashboard-products")


@login_required
@user_passes_test(is_employee)
def product_detail(request, pk):
    context = {}
    return render(request, "dashboard/products_detail.html", context)


@login_required
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
def meal_category_delete(request, pk):
    category = get_object_or_404(MealCategory, pk=pk)
    category.delete()

    return redirect("dashboard-meal_categories")


@login_required
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
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
@user_passes_test(is_employee)
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    meal.delete()

    return redirect("dashboard-meals")


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def customers(request):

    users = User.objects.filter(groups=Group.objects.get(name="Customers"))
    context = {
        "users": users,
    }

    return render(request, "dashboard/customers.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def employees(request):

    users = User.objects.filter(groups=Group.objects.get(name="Employees"))
    context = {
        "users": users,
    }

    return render(request, "dashboard/employees.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def admins(request):

    users = User.objects.filter(groups=Group.objects.get(name="Admin"))
    context = {
        "users": users,
    }

    return render(request, "dashboard/employees.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def purchases(request):
    sales = TicketSales.objects.all()
    context = {
        "sales": sales,
    }
    return render(request, "dashboard/purchases.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
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
    current_group = user.groups.first()

    if request.method == "POST":
        form = ChangeUserGroupForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data["group"]
            # Remove user from all groups and add to the selected one
            user.groups.clear()
            user.groups.add(group)
            match group.name:
                case "Admin":
                    return redirect("dashboard-admins")
                case "Employees":
                    return redirect("dashboard-employees")
                case "Customers":
                    return redirect("dashboard-customers")
    form = ChangeUserGroupForm(initial_group=current_group)
    context = {
        "form": form,
        "user_profile": user,
    }
    return render(request, "dashboard/user_detail.html", context)


@login_required
@user_passes_test(is_employee)
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
            voucher_no=payment_id,
            type=payment_type,
            status=payment_status,
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


def payments(request):

    data = []
    for payment in Payments.objects.all():
        if TicketSales.objects.filter(payment=payment).exists():
            sale_id = TicketSales.objects.get(payment=payment).id
            data.append({"payment": payment, "sale_id": sale_id, "type": "T"})
        else:
            sale_id = PurchaseReceipt.objects.get(payment=payment).id
            data.append({"payment": payment, "sale_id": sale_id, "type": "P"})

    return render(request, "dashboard/payments.html", {"data": data})


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
def journeys(request):
    context = {
        "product": Product.objects.all(),
        "order": Order.objects.all(),
    }
    return render(request, "dashboard/journeys.html", context)


@login_required
@user_passes_test(is_employee)
def transports(request):
    context = {
        "product": Product.objects.all(),
        "order": Order.objects.all(),
    }
    return render(request, "dashboard/transports.html", context)


@login_required
@user_passes_test(is_employee)
def planning(request):
    context = {
        "product": Product.objects.all(),
        "order": Order.objects.all(),
    }
    return render(request, "dashboard/planning.html", context)


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


def prueba(request):
    return render(request, "public/Untitled-1.html")


@login_required
@user_passes_test(is_employee)
def receipts(request):
    context = {"receipts": PurchaseReceipt.objects.all()}
    return render(request, "dashboard/receipts.html", context)


@login_required
@user_passes_test(is_employee)
def receipt_payment(request, sale_id):
    if PurchaseReceipt.objects.get(id=sale_id).payment:
        return render(
            request,
            "dashboard/purchase_detail.html",
            {"payment": PurchaseReceipt.objects.get(id=sale_id).payment},
        )
    return render(request, "dashboard/purchase_detail.html", {})


@login_required
@user_passes_test(is_employee)
def receipt_detail(request, sale_id):
    receipt = PurchaseReceipt.objects.get(id=sale_id)
    if DetailFoodOrder.objects.filter(receipt=receipt).exists():
        context = {"details": DetailFoodOrder.objects.filter(receipt=receipt)}
    else:
        context = {"details": DetailsProductOrder.objects.filter(receipt=receipt)}
    return render(request, "dashboard/receipt_detail.html", context)


@login_required
@user_passes_test(is_employee)
def journey_prices(request):
    prices = JourneyPrices.objects.all()

    if request.method == "POST":
        form = JourneyPricesForm(request.POST)
        if form.is_valid():
            form.save()
            category_name = form.cleaned_data.get("type")
            messages.success(request, f"{category_name} has been added")
            return redirect("dashboard-journey_prices")
    else:
        form = JourneyPricesForm()
    context = {
        "prices": prices,
        "form": form,
    }
    return render(request, "dashboard/journey_prices.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def journey_price_edit(request, pk):
    item = JourneyPrices.objects.get(id=pk)
    if request.method == "POST":
        form = JourneyPricesForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-journey_prices")
    else:
        form = JourneyPricesForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def journey_price_delete(request, pk):
    price = get_object_or_404(JourneyPrices, pk=pk)
    price.delete()

    return redirect("dashboard-journey_prices")


@login_required
@user_passes_test(is_employee)
def seats(request):
    seats = Seat.objects.all()

    if request.method == "POST":
        form = SeatForm(request.POST)
        if form.is_valid():
            form.save()
            seat_name = form.cleaned_data.get("seat_number")
            messages.success(request, f"{seat_name} has been added")
            return redirect("dashboard-seats")
    else:
        form = SeatForm()
    context = {
        "seats": seats,
        "form": form,
    }
    return render(request, "dashboard/seats.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def seat_edit(request, pk):
    item = Seat.objects.get(id=pk)
    if request.method == "POST":
        form = SeatForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-seats")
    else:
        form = SeatForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def seat_delete(request, pk):
    item = get_object_or_404(Seat, pk=pk)
    item.delete()

    return redirect("dashboard-seats")


@login_required
@user_passes_test(is_employee)
def buses(request):
    buses = Bus.objects.all()

    if request.method == "POST":
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            bus_name = form.cleaned_data.get("name")
            messages.success(request, f"{bus_name} has been added")
            return redirect("dashboard-buses")
    else:
        form = BusForm()
    context = {
        "blocktitle": _("Buses"),
        "topside": "partials/topside_transports.html",
        "title_form": _("Add New Bus"),
        "columns": [
            "ID",
            _("Name"),
            _("Capacity"),
        ],
        "atributes": ["id", "name", "capacity"],
        "url_edit": "dashboard-bus-edit",
        "url_delete": "dashboard-bus-delete",
        "items": buses,
        "form": form,
    }
    return render(request, "dashboard/base_table.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def bus_edit(request, pk):
    item = Bus.objects.get(id=pk)
    if request.method == "POST":
        form = BusForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-buses")
    else:
        form = BusForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def bus_delete(request, pk):
    item = get_object_or_404(Bus, pk=pk)
    item.delete()

    return redirect("dashboard-buses")


@login_required
@user_passes_test(is_employee)
def trains(request):
    trains = Train.objects.all()

    if request.method == "POST":
        form = TrainForm(request.POST)
        if form.is_valid():
            form.save()
            train_name = form.cleaned_data.get("name")
            messages.success(request, f"{train_name} has been added")
            return redirect("dashboard-trains")
    else:
        form = TrainForm()
    context = {
        "blocktitle": _("Trains"),
        "topside": "partials/topside_transports.html",
        "title_form": _("Add New Train"),
        "columns": [
            "ID",
            _("Name"),
            _("Capacity"),
        ],
        "atributes": ["id", "name", "capacity"],
        "url_edit": "dashboard-train-edit",
        "url_delete": "dashboard-train-delete",
        "items": trains,
        "form": form,
    }
    return render(request, "dashboard/base_table.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def train_edit(request, pk):
    item = Train.objects.get(id=pk)
    if request.method == "POST":
        form = TrainForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-trains")
    else:
        form = TrainForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def train_delete(request, pk):
    item = get_object_or_404(Train, pk=pk)
    item.delete()

    return redirect("dashboard-trains")


@login_required
@user_passes_test(is_employee)
def types_journey(request):
    types_journey = Journey.objects.all()

    if request.method == "POST":
        form = JourneyForm(request.POST)
        if form.is_valid():
            form.save()
            journey_name = form.cleaned_data.get("type")
            messages.success(request, f"{journey_name} has been added")
            return redirect("dashboard-types_journey")
    else:
        form = JourneyForm()
    context = {
        "blocktitle": _("Types Journey"),
        "topside": "partials/topside_planning.html",
        "title_form": _("Add New Journey"),
        "columns": [
            "ID",
            _("Type"),
            _("Description"),
        ],
        "atributes": ["id", "type", "description"],
        "url_edit": "dashboard-type_journey-edit",
        "url_delete": "dashboard-type_journey-delete",
        "items": types_journey,
        "form": form,
    }
    return render(request, "dashboard/base_table.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def type_journey_edit(request, pk):
    item = Journey.objects.get(id=pk)
    if request.method == "POST":
        form = JourneyForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-types_journey")
    else:
        form = JourneyForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def type_journey_delete(request, pk):
    item = get_object_or_404(Journey, pk=pk)
    item.delete()

    return redirect("dashboard-types_journey")


@login_required
@user_passes_test(is_employee)
def journey_stages(request):
    journey_stages = JourneyStage.objects.all()

    if request.method == "POST":
        form = JourneyStageForm(request.POST)
        if form.is_valid():
            form.save()
            journeystage_name = form.cleaned_data.get("name")
            messages.success(request, f"{journeystage_name} has been added")
            return redirect("dashboard-journey_stages")
    else:
        form = JourneyStageForm()
    context = {
        "blocktitle": _("Journey Stages"),
        "topside": "partials/topside_planning.html",
        "title_form": _("Add New Journey Stage"),
        "columns": [
            _("Journey"),
            _("Order"),
            _("Departure Stop"),
            _("Arrival Stop"),
            _("Transport"),
            _("Duration"),
        ],
        "atributes": [
            "journey",
            "order",
            "departure_stop",
            "arrival_stop",
            "transport",
            "duration",
        ],
        "url_edit": "dashboard-journey_stage-edit",
        "url_delete": "dashboard-journey_stage-delete",
        "items": journey_stages,
        "form": form,
    }
    return render(request, "dashboard/base_table.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def journey_stage_edit(request, pk):
    item = JourneyStage.objects.get(id=pk)
    if request.method == "POST":
        form = JourneyStageForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-journey_stages")
    else:
        form = JourneyStageForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def journey_stage_delete(request, pk):
    item = get_object_or_404(JourneyStage, pk=pk)
    item.delete()

    return redirect("dashboard-journey_stages")


@login_required
@user_passes_test(is_employee)
def journey_schedules(request):
    journey_schedules = JourneySchedule.objects.all()

    if request.method == "POST":
        form = JourneyScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            journey_schedule_name = form.cleaned_data.get("name")
            messages.success(request, f"{journey_schedule_name} has been added")
            return redirect("dashboard-journey_schedules")
    else:
        form = JourneyScheduleForm()
    context = {
        "blocktitle": _("Journey Schedule"),
        "topside": "partials/topside_planning.html",
        "title_form": _("Add New Journey Schedule"),
        "columns": [
            _("Journey"),
            _("Departure Time"),
            _("Arrival Time"),
        ],
        "atributes": ["journey", "departure_time", "arrival_time"],
        "url_edit": "dashboard-journey_schedule-edit",
        "url_delete": "dashboard-journey_schedule-delete",
        "items": journey_schedules,
        "form": form,
    }
    return render(request, "dashboard/base_table.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def journey_schedule_edit(request, pk):
    item = JourneySchedule.objects.get(id=pk)
    if request.method == "POST":
        form = JourneyScheduleForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-journey_schedules")
    else:
        form = JourneyScheduleForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def journey_schedule_delete(request, pk):
    item = get_object_or_404(JourneySchedule, pk=pk)
    item.delete()

    return redirect("dashboard-journey_schedules")


@login_required
@user_passes_test(is_employee)
def stops(request):
    stops = Stops.objects.all()

    if request.method == "POST":
        form = StopForm(request.POST)
        if form.is_valid():
            form.save()
            stop_name = form.cleaned_data.get("name")
            messages.success(request, f"{stop_name} has been added")
            return redirect("dashboard-stops")
    else:
        form = StopForm()
    context = {
        "blocktitle": _("Stops"),
        "topside": "partials/topside_planning.html",
        "title_form": _("Add New Stop"),
        "columns": [
            _("Name"),
            _("Location"),
            _("Type"),
        ],
        "atributes": ["name", "location", "type"],
        "url_edit": "dashboard-stop-edit",
        "url_delete": "dashboard-stop-delete",
        "items": stops,
        "form": form,
    }
    return render(request, "dashboard/base_table.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def stop_edit(request, pk):
    item = Stops.objects.get(id=pk)
    if request.method == "POST":
        form = StopForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard-stops")
    else:
        form = StopForm(instance=item)
    context = {
        "form": form,
    }
    return render(request, "dashboard/item_edit.html", context)


@login_required(login_url="user-login")
@user_passes_test(is_employee)
def stop_delete(request, pk):
    item = get_object_or_404(Stops, pk=pk)
    item.delete()

    return redirect("dashboard-stops")


def api_product_categories(request):
    return JsonResponse(
        list(ProductCategory.objects.all().values("id", "name")), safe=False
    )


def api_type_payment(request):
    types = []
    for type in Payments.TYPES:
        types.append([type[0], type[1]])
    return JsonResponse(types, safe=False)


def api_products_per_category(request):
    category_id = request.GET.get("category_id")
    return JsonResponse(
        list(
            Product.objects.filter(category=category_id).values("id", "name", "price")
        ),
        safe=False,
    )


@require_http_methods(["POST"])
def api_register_sale_products(request):
    try:
        data = json.loads(request.body)
        id_pasajero = data.get("id_pasajero")
        productos = data.get("productos")
        type_payment = data.get("metodo_pago")
        voucher_no = data.get("nro_comprobante")

        if voucher_no:
            payment = Payments.objects.create(type=type_payment, voucher_no=voucher_no)
        else:
            payment = Payments.objects.create(type=type_payment)

        sale = PurchaseReceipt.objects.create(
            passenger=Passenger.objects.get(dni_or_passport=id_pasajero),
            payment=payment,
        )
        for product in productos:
            DetailsProductOrder.objects.create(
                receipt=sale,
                product=Product.objects.get(id=product["producto_id"]),
                quantity=int(product["cantidad"]),
            )

        return JsonResponse(
            {
                "msg": "Venta registrada con éxito.",
            },
            status=200,
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        if str(e) == "Passenger matching query does not exist.":
            msg = _("Passenger not exist")
        else:
            msg = _("Something went wrong")
        return JsonResponse(
            {
                "error": msg,
            },
            status=400,
        )


def product_sales(request):
    return render(request, "dashboard/product_sales.html")


# Cambio
def api_meal_categories(request):
    return JsonResponse(
        list(MealCategory.objects.all().values("id", "name")), safe=False
    )


def api_meals_per_category(request):
    category_id = request.GET.get("category_id")
    return JsonResponse(
        list(Meal.objects.filter(category=category_id).values("id", "name", "price")),
        safe=False,
    )


@require_http_methods(["POST"])
def api_register_sale_meals(request):
    try:
        data = json.loads(request.body)
        id_pasajero = data.get("id_pasajero")
        productos = data.get("productos")
        type_payment = data.get("metodo_pago")
        voucher_no = data.get("nro_comprobante")

        if voucher_no:
            payment = Payments.objects.create(type=type_payment, voucher_no=voucher_no)
        else:
            payment = Payments.objects.create(type=type_payment)

        sale = PurchaseReceipt.objects.create(
            passenger=Passenger.objects.get(dni_or_passport=id_pasajero),
            payment=payment,
        )
        for product in productos:
            DetailFoodOrder.objects.create(
                receipt=sale,
                meal=Meal.objects.get(id=product["producto_id"]),
                quantity=int(product["cantidad"]),
            )

        return JsonResponse(
            {
                "msg": _("Venta registrada con éxito."),
            },
            status=200,
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        if str(e) == "Passenger matching query does not exist.":
            msg = _("Passenger not exist")
        else:
            msg = _("Something went wrong")
        return JsonResponse(
            {
                "error": msg,
            },
            status=400,
        )


def register_sales_meals(request):
    context = {
        "title": _("Orden de Compra de Comidas"),
        "model_singular": _("Comida"),
        "get_categories": "api_meal_categories",
        "get_product_per_category": "api_meals_per_category",
        "register_sale": "api_register_sale_meals",
    }
    return render(request, "dashboard/register_sale.html", context)


def register_sales_products(request):
    context = {
        "title": _("Orden de Compra de Productos"),
        "model_singular": _("Producto"),
        "get_categories": "api_product_categories",
        "get_product_per_category": "api_products_per_category",
        "register_sale": "api_register_sale_products",
    }
    return render(request, "dashboard/register_sale.html", context)


def api_types_journey(request):
    types = []
    for type in Journey.JOURNEY_TYPE_CHOICES:
        types.append([type[0], type[1]])
    return JsonResponse(types, safe=False)


def api_journey_per_date(request):
    fecha = request.GET.get("fecha")
    type = request.GET.get("tipo_recorrido")
    # Parámetros
    schedules = JourneySchedule.getSchedules(type, fecha)
    return JsonResponse(schedules, safe=False)


def tickets_reserve(request):
    return render(request, "public/ticket_reserve.html")


def api_available_seats_per_schedule(request):
    categoria = request.GET.get("categoria")
    horario = request.GET.get("horario")

    schedule = JourneySchedule.objects.get(id=horario)
    seats = Ticket.objects.filter(schedule=schedule)
    category = JourneyPrices.objects.get(id=categoria).category
    seatsfilter = []
    response = []
    print(list(seats))
    if list(seats) != []:
        for seat in seats:
            if seat.seat.category == category:
                seatsfilter.append(seat.seat)

        if seatsfilter != []:
            tranport = seatsfilter[0].transport

            seats_transport_category = Seat.objects.filter(
                transport=tranport, category=category
            )

            for seat in seats_transport_category:
                if seat not in seatsfilter:
                    response.append({"id": seat.id, "numero": seat.seat_number})
    else:
        seats = Seat.objects.filter(category=category)
        for seat in seats:
            response.append({"id": seat.id, "numero": seat.seat_number})
    return JsonResponse(response, safe=False)


def api_price_journey(request):
    type = request.GET.get("tipo_recorrido")
    print(type)
    journey = Journey.objects.get(type=type)
    prices = JourneyPrices.objects.filter(journey=journey)
    response = []
    for price in prices:
        response.append(
            {
                "id": price.id,
                "category": price.getCategory(),
                "price": price.price,
            }
        )
    return JsonResponse(
        response,
        safe=False,
    )


@require_http_methods(["GET", "POST"])
@transaction.atomic
def api_reserve_tickets(request):
    data = json.loads(request.body)
    email = data.get("email")
    tickets = data.get("pasajeros")
    user = data.get("id_user")

    if user:
        user = User.objects.get(id=user)
        sale = TicketSales.objects.create(email=email, user=user)
    else:
        sale = TicketSales.objects.create(email=email)

    for ticket in tickets:
        schedule = JourneySchedule.objects.get(id=ticket["horario"])
        seat = Seat.objects.get(id=ticket["asiento"])
        passenger = Passenger.objects.filter(
            dni_or_passport=ticket["dni_o_pasaporte"]
        ).first()
        Ticket.objects.create(
            sale=sale, passenger=passenger, schedule=schedule, seat=seat
        )

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
            "success": request.build_absolute_uri(reverse("payment_success")),
            "failure": request.build_absolute_uri(reverse("payment_pending")),
            "pending": request.build_absolute_uri(reverse("payment_pending")),
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
