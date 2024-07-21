from django import forms
from django.forms.widgets import NumberInput

# Autenticacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Formularios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder

# Modelos
from .models import *

# Vistas
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

# Traducciones
from django.utils.translation import gettext as _


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["name", "order_quantity"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label=_("Correo electrónico"))
    first_name = forms.CharField(label=_("Nombre"))
    last_name = forms.CharField(label=_("Apellido"))

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "username": _("Username"),
            "email": _("email"),
            "first_name": _("first name"),
            "last_name": _("last name"),
            "password1": _("password"),
            "password2": _("confirm password"),
        }

    def clean_email(self):
        email_field = self.cleaned_data["email"]

        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado")

        return email_field


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            "name",
            "dni_or_passport",
            "emergency_telephone",
            "date_of_birth",
            "gender",
            "origin_country",
        ]
        labels = {
            "name": _("Name"),
            "dni_or_passport": _("DNI/Passport"),
            "emergency_telephone": _("Emergency Telephone"),
            "date_of_birth": _("Date of Birth"),
            "gender": _("Gender"),
            "origin_country": _("Origin Country"),
        }
        widgets = {
            "date_of_birth": NumberInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class TicketSalesForm(forms.ModelForm):
    email = forms.EmailField(required=False, label=_("Email (if not logged in)"))

    class Meta:
        model = TicketSales
        fields = [
            "email",
        ]
        labels = {
            "email": _("Email"),
        }


class TicketForm(forms.ModelForm):
    dni_or_passport = forms.CharField(
        max_length=50,
        label=_("DNI/Passport"),
        widget=forms.TextInput(attrs={"class": "dni_or_passport"}),
    )

    class Meta:
        model = Ticket
        fields = ["dni_or_passport", "schedule", "seat"]
        labels = {
            "dni_or_passport": _("DNI/Passport"),
            "schedule": _("Schedule"),
            "seat": _("Seat"),
        }


TicketFormSet = inlineformset_factory(
    TicketSales,
    Ticket,
    form=TicketForm,
    fields=["dni_or_passport", "schedule", "seat"],
    extra=1,
    can_delete=True,
)


class TicketFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.layout = Layout(
            Fieldset("Tickets", "passenger", "schedule", "seat"),
            ButtonHolder(
                Submit("submit", "Purchase Tickets", css_class="btn btn-primary")
            ),
        )
        self.render_required_fields = True
        self.form_tag = True


class PurchaseReceiptForm(forms.ModelForm):
    dni_or_passport = forms.CharField(max_length=50, label="DNI/Passport")

    class Meta:
        model = PurchaseReceipt
        fields = [
            "dni_or_passport",
        ]
        labels = {
            "dni_or_passport": _("DNI/Passport"),
        }


class DetailFoodOrderForm(forms.ModelForm):
    class Meta:
        model = DetailFoodOrder
        fields = ["meal", "quantity"]
        labels = {
            "meal": _("Meal"),
            "quantity": _("Quantity"),
        }


DetailFoodOrderFormSet = inlineformset_factory(
    PurchaseReceipt,
    DetailFoodOrder,
    form=DetailFoodOrderForm,
    fields=["meal", "quantity"],
    extra=1,
    can_delete=True,
)


class DetailsProductOrderForm(forms.ModelForm):
    class Meta:
        model = DetailsProductOrder
        fields = ["product", "quantity"]
        labels = {
            "product": _("product"),
            "quantity": _("Quantity"),
        }


DetailsProductOrderSet = inlineformset_factory(
    PurchaseReceipt,
    DetailsProductOrder,
    form=DetailsProductOrderForm,
    fields=["product", "quantity"],
    extra=1,
    can_delete=True,
)


class JourneyScheduleForm(forms.ModelForm):
    class Meta:
        model = JourneySchedule
        fields = [
            "journey",
            "departure_time",
            "arrival_time",
        ]
        labels = {
            "journey": _("Journey"),
            "departure_time": _("Departure Time"),
            "arrival_time": _("Arrival Time"),
        }
        widgets = {
            "departure_time": NumberInput(attrs={"type": "datetime"}),
            "arrival_time": NumberInput(attrs={"type": "datetime"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
        ]
        labels = {
            "name": _("Name"),
            "price": _("Price"),
            "description": _("Description"),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = [
            "name",
            "category",
            "price",
        ]
        labels = {
            "name": _("Name"),
            "category": _("Category"),
            "price": _("Price"),
        }


class MealCategoryForm(forms.ModelForm):
    class Meta:
        model = MealCategory
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }
