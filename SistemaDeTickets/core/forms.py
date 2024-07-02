from django import forms

# Autenticacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Formularios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder

# Modelos
from .models import (
    Passenger,
    Ticket,
    TicketSales,
    PurchaseReceipt,
    DetailFoodOrder,
    DetailsMerchandiseOrder,
)

# Vistas
from django.forms import modelformset_factory
from django.forms import inlineformset_factory


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class TicketSalesForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="Email (if not logged in)")

    class Meta:
        model = TicketSales
        fields = [
            "email",
        ]


class TicketForm(forms.ModelForm):
    dni_or_passport = forms.CharField(
        max_length=50,
        label="DNI/Passport",
        widget=forms.TextInput(attrs={"class": "dni_or_passport"}),
    )

    class Meta:
        model = Ticket
        fields = ["dni_or_passport", "schedule", "seat"]


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


class DetailFoodOrderForm(forms.ModelForm):
    class Meta:
        model = DetailFoodOrder
        fields = ["meal", "quantity"]


DetailFoodOrderFormSet = inlineformset_factory(
    PurchaseReceipt,
    DetailFoodOrder,
    form=DetailFoodOrderForm,
    fields=["meal", "quantity"],
    extra=1,
    can_delete=True,
)


class DetailsMerchandiseOrderForm(forms.ModelForm):
    class Meta:
        model = DetailsMerchandiseOrder
        fields = ["merchandise", "quantity"]


DetailsMerchandiseOrderSet = inlineformset_factory(
    PurchaseReceipt,
    DetailsMerchandiseOrder,
    form=DetailsMerchandiseOrderForm,
    fields=["merchandise", "quantity"],
    extra=1,
    can_delete=True,
)
