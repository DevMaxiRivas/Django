from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

# Traducciones
from django.utils.translation import gettext as _

# Horarios
from django.utils import timezone

# DataBase
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

STATES1 = (
    ("h", _("Habilitado")),
    ("d", _("Deshabilitado")),
)


class Stops(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100)
    location = models.CharField(verbose_name=_("location"), max_length=255)
    type = models.CharField(
        verbose_name=_("type"),
        max_length=1,
        choices=(
            ("b", _("Bus")),
            ("t", _("Train")),
        ),
        blank=True,
        default="t",
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Stop")
        verbose_name_plural = _("Stops")

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.hab_pv)
        return None


class Transport(models.Model):
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def __str__(self):
        if Train.objects.filter(transport=self).exists():
            return f"ID Transport {self.id} - Train {Train.objects.get(transport=self).name}"
        return f"ID Transport {self.id} - Bus {Bus.objects.get(transport=self).name}"


class Train(models.Model):
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name=_("name"), max_length=100)
    capacity = models.PositiveIntegerField(
        verbose_name=_("capacity"), blank=True, null=True
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def save(self, *args, **kwargs):
        if not self.transport:
            self.transport = Transport.objects.create()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Train")
        verbose_name_plural = _("Trains")

    def __str__(self):
        return self.name


class Bus(models.Model):
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name=_("name"), max_length=100)
    capacity = models.PositiveIntegerField(
        verbose_name=_("capacity"), blank=True, null=True
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["name"]
        verbose_name = _("Bus")
        verbose_name_plural = _("Buses")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.transport:
            self.transport = Transport.objects.create()
        super().save(*args, **kwargs)


class SeatCategory(models.Model):
    type = models.CharField(
        verbose_name=_("type"), max_length=100, null=True, blank=True
    )
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:

            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["type"]
        verbose_name = _("Seat Category")
        verbose_name_plural = _("Seat Categories")

    def __str__(self):
        return self.type

class Seat(models.Model):
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        related_name="seats",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    seat_number = models.CharField(verbose_name=_("seat_number"), max_length=10)
    category = models.ForeignKey(
        SeatCategory,
        verbose_name=_("category"),
        related_name="seats",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:

            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    # def save(self, *args, **kwargs):
    #         # Si es el mismo asiento con el que se creo la venta no modificar el precio
    #         if self._state.adding:
    #             if self.ve_bl:
    #                 self.cli_bl = self.ve_bl.cli_ve
    #                 self.evt_bl = self.ve_bl.evt_ve

    #         super().save(*args, **kwargs)

    class Meta:
        ordering = ["seat_number"]
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")

    def __str__(self):
        return f"{self.seat_number} ({self.category.type})"


class MealCategory(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50, null=True)
    description = models.TextField(verbose_name=_("description"), null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Meal Category")
        verbose_name_plural = _("Meal Categories")


class Meal(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100)
    category = models.ForeignKey(
        MealCategory,
        verbose_name=_("category"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name=_("description"), null=True)
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return self.name

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None


class ProductCategory(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50, null=True)
    description = models.TextField(verbose_name=_("description"), null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")


class Product(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100, null=True)
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    description = models.TextField(verbose_name=_("description"), null=True)
    stock = models.PositiveIntegerField(verbose_name=_("stock"), default=1)
    category = models.ForeignKey(
        ProductCategory, verbose_name=_("category"), on_delete=models.CASCADE, null=True
    )
    state = models.CharField(
        verbose_name=_("state"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.customer}-{self.name}"


class Journey(models.Model):
    JOURNEY_TYPE_CHOICES = [
        ("TRAIN_ONLY", "Train Only"),
        ("BUS_AND_TRAIN", "Bus and Train"),
    ]

    type = models.CharField(
        verbose_name=_("type"), max_length=20, choices=JOURNEY_TYPE_CHOICES
    )
    description = models.TextField(verbose_name=_("description"))

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )
    #Funciones
    def passengers_for_journey():
        return Journey.objects.values('type').annotate(
            total_passengers=Count('journeyschedule__ticket__passenger')
        )
    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["type"]
        verbose_name = _("Journey")
        verbose_name_plural = _("Journeys")

    def __str__(self):
        return f"{self.type}"


class JourneyStage(models.Model):
    journey = models.ForeignKey(
        Journey,
        verbose_name=_("journey"),
        related_name="stages",
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField()
    departure_stop = models.ForeignKey(
        Stops,
        verbose_name=_("departure_stop"),
        related_name="start_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    arrival_stop = models.ForeignKey(
        Stops,
        verbose_name=_("arrival_stop"),
        related_name="end_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    duration = models.DurationField(verbose_name=_("duration"))

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["order"]
        verbose_name = _("Journey Stage")
        verbose_name_plural = _("Journey Stages")

    def __str__(self):
        return f"{self.journey} - Stage {self.order}"


class JourneySchedule(models.Model):
    journey = models.ForeignKey(
        Journey, verbose_name=_("journey"), on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField(verbose_name=_("departure_time"))
    arrival_time = models.DateTimeField(verbose_name=_("arrival_time"))

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["journey"]
        verbose_name = _("Journey Schedule")
        verbose_name_plural = _("Journey Schedules")

    def __str__(self):
        return f"{self.journey} - {timezone.localtime(self.departure_time).strftime("%Y-%m-%d %H:%M")}"


class Passenger(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100)
    dni_or_passport = models.CharField(verbose_name=_("dni_or_passport"), max_length=50)
    origin_country = models.CharField(verbose_name=_("origin_country"), max_length=100)
    emergency_telephone = models.CharField(
        verbose_name=_("emergency_telephone"), max_length=50, null=True, blank=True
    )
    date_of_birth = models.DateField(
        verbose_name=_("date_of_birth"), null=True, blank=True
    )
    # Telefono (Emergencia)
    # Fecha de Nacimiento
    GENDER = (
        ("m", "Male"),
        ("w", "Female"),
    )

    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=1,
        choices=GENDER,
        blank=True,
        default="m",
        help_text="Genero del pasajero",
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["dni_or_passport"]
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")

    def __str__(self):
        return self.name

class Payments(models.Model):
    payment_id = models.CharField(verbose_name=_("payment_id"), max_length=255)
    payment_type = models.CharField(verbose_name=_("payment_type"), max_length=50)
    payment_status = models.CharField(
        verbose_name=_("payment_status"), max_length=50, null=True, blank=True
    )

    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)

    def __str__(self):
        if self.payment_id and self.payment_type:
            return f"Pago {self.payment_id} - {self.payment_type}"
        return "Pago" + self.created_at

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Payments")
        verbose_name_plural = _("Payments")


class TicketSales(models.Model):
    email = models.EmailField(verbose_name=_("email"), null=True, blank=True)
    user = models.ForeignKey(
        User, verbose_name=_("user"), on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    purchase_date = models.DateTimeField(
        verbose_name=_("purchase_date"), default=timezone.now
    )
    payment = models.ForeignKey(
        Payments,
        verbose_name=_("payment"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def update_total_price(self):
        self.price = sum(ticket.price for ticket in self.tickets.all())
        self.save()

    def __str__(self):
        if self.user:
            return f"Sale for {self.user.username} on {self.purchase_date}"
        return f"Sale on {self.purchase_date}"
    
    def ventas_por_año():
        hace_un_año = timezone.now() - timedelta(days=365)
        ventas = TicketSales.objects.filter(purchase_date__gte=hace_un_año)
        ventas_por_mes = ventas.annotate(mes=TruncMonth('purchase_date')).values('mes').annotate(cantidad=Count('id')).order_by('mes')
        return ventas_por_mes

    class Meta:
        ordering = ["user"]
        verbose_name = _("Ticket Sale")
        verbose_name_plural = _("Ticket Sales")


class Ticket(models.Model):
    sale = models.ForeignKey(
        TicketSales,
        verbose_name=_("sale"),
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    passenger = models.ForeignKey(
        Passenger, verbose_name=_("passenger"), on_delete=models.CASCADE
    )
    schedule = models.ForeignKey(
        JourneySchedule, verbose_name=_("schedule"), on_delete=models.CASCADE
    )
    seat = models.ForeignKey(Seat, verbose_name=_("seat"), on_delete=models.CASCADE)
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f"Ticket for {self.passenger.name} purchased by {self.user.username}"
    
    # Funciones
    def revenue_by_seat_category():
        return Ticket.objects.values('seat__category__type').annotate(total_ingresos=Sum('price')).order_by('-total_ingresos')

    # Funcion para reservar el asiento
    def reserveSeat(self):
        asiento = self.seat
        asiento.status = "v"
        asiento.save()

    def save(self, *args, **kwargs):
        # Si es el mismo asiento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.seat:
                self.price = self.seat.category.price
        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = Ticket.objects.get(pk=self.pk)
            if old_instance.seat != self.seat:
                self.price = self.seat.category.price

        # self.reserveSeat()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Cambiar el campo status del asiento asociado a 'h' antes de eliminar el ticket
        self.seat.status = "h"
        self.seat.save()
        super().delete(*args, **kwargs)

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def __str__(self):
        return f"Ticket for {self.passenger.name}"

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class PurchaseReceipt(models.Model):
    passenger = models.ForeignKey(
        Passenger,
        verbose_name=_("passenger"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    purchase_date = models.DateTimeField(
        verbose_name=_("purchase_date"), default=timezone.now
    )
    payment = models.ForeignKey(
        Payments,
        verbose_name=_("payment"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def update_total_price(self):
        self.price = sum(meal.unit_price * meal.quantity for meal in self.meals.all())
        self.save()

    def update_total_price_of_product(self):
        self.price = sum(
            product.unit_price * product.quantity for product in self.products.all()
        )
        self.save()

    def __str__(self):
        if self.passenger:
            return f"Sale for {self.passenger.name} on {self.purchase_date}"
        return f"Sale on {self.purchase_date}"

    class Meta:
        ordering = ["purchase_date"]
        verbose_name = _("Purchase Receipt")
        verbose_name_plural = _("Purchase Receipts")


class DetailFoodOrder(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt,
        verbose_name=_("receipt"),
        related_name="meals",
        on_delete=models.CASCADE,
    )
    meal = models.ForeignKey(Meal, verbose_name=_("meal"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default=1)
    unit_price = models.DecimalField(
        verbose_name=_("unit_price"), max_digits=10, decimal_places=2, default=0
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def delete(self, *args, **kwargs):
        # Cambiar el campo status del asiento asociado a 'h' antes de eliminar el ticket
        self.receipt.price = self.receipt.price - self.unit_price * self.quantity
        self.receipt.save()
        super().delete(*args, **kwargs)

    def update_receipt(self):
        receipt = self.receipt
        receipt.price = receipt.price + (self.unit_price * self.quantity)
        receipt.save()

    def save(self, *args, **kwargs):
        # Si es el mismo asiento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.meal:
                self.unit_price = self.meal.price
                self.update_receipt()

        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = DetailFoodOrder.objects.get(pk=self.pk)
            if old_instance.meal != self.meal:
                # Quitar mercaderia del recibo
                self.receipt.price = self.receipt.price - (
                    old_instance.unit_price * old_instance.quantity
                )
                self.unit_price = self.meal.price
                self.update_receipt()

        super().save(*args, **kwargs)

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def __str__(self):
        return f"{self.quantity} x {self.meal.name}"

    class Meta:
        ordering = ["receipt"]
        verbose_name = _("Detail Food Order")
        verbose_name_plural = _("Detail Food Orders")


class DetailsProductOrder(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt,
        verbose_name=_("receipt"),
        related_name="products",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, verbose_name=_("product"), on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default=1)
    unit_price = models.DecimalField(
        verbose_name=_("unit_price"), max_digits=10, decimal_places=2, default=0
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )
    # Funciones
    def revenue_per_product():
        return DetailsProductOrder.objects.values('product__name').annotate(total_ingresos=Sum('unit_price * quantity')).order_by('-total_ingresos')


    def delete(self, *args, **kwargs):
        # Cambiar el campo status del asiento asociado a 'h' antes de eliminar el ticket
        self.receipt.price = self.receipt.price - self.unit_price * self.quantity
        self.receipt.save()
        super().delete(*args, **kwargs)

    def update_receipt(self):
        receipt = self.receipt
        receipt.price = receipt.price + (self.unit_price * self.quantity)
        receipt.save()

    def save(self, *args, **kwargs):
        # Si es el mismo asiento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.product:
                self.unit_price = self.product.price
                self.update_receipt()

        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = DetailsProductOrder.objects.get(pk=self.pk)
            if old_instance.product != self.product:
                # Quitar mercaderia del recibo
                self.receipt.price = self.receipt.price - (
                    old_instance.unit_price * old_instance.quantity
                )
                self.unit_price = self.product.price
                self.update_receipt()

        super().save(*args, **kwargs)

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["receipt"]
        verbose_name = _("Details Product Order")
        verbose_name_plural = _("Details Product Orders")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
