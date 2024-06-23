from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Ticket, Passenger, TicketSales


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


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Passenger, Ticket, TicketSales


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ["name", "dni_or_passport", "gender", "origin_country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


from django import forms
from django.forms import modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Ticket, Passenger, JourneySchedule, Seat


class TicketForm(forms.ModelForm):
    passenger = forms.ModelChoiceField(queryset=Passenger.objects.filter(enabled="h"))
    schedule = forms.ModelChoiceField(
        queryset=JourneySchedule.objects.filter(enabled="h")
    )
    seat = forms.ModelChoiceField(
        queryset=Seat.objects.filter(enabled="h", is_reserved=False)
    )

    class Meta:
        model = Ticket
        fields = ["passenger", "schedule", "seat"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Ticket Information", "passenger", "schedule", "seat")
        )


TicketFormSet = modelformset_factory(Ticket, form=TicketForm, extra=1, can_delete=True)


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
