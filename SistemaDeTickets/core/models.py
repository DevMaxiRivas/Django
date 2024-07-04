from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid  # Requerida para las instancias de tuplas únicas

from django.conf import settings


STATES1 = (
    ("h", "Habilitado"),
    ("d", "Desahabilitado"),
)

STATES2 = (
    ("h", "Habilitado"),
    ("d", "Desahabilitado"),
    ("s", "Suspendido"),
    ("f", "Finalizado"),
)

STATES3 = (
    ("h", "Habilitado"),
    ("d", "Desahabilitado"),
    ("v", "Vendido"),
    ("r", "Devuelto"),
)


class Station(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Estacion"
        verbose_name_plural = "Estaciones"

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.hab_pv)
        return None


class BusStop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Parada de colectivo"
        verbose_name_plural = "Paradas de colectivo"

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["name"]
        verbose_name = "Tren"
        verbose_name_plural = "Trenes"

    def __str__(self):
        return self.name


class Bus(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["name"]
        verbose_name = "Colectivo"
        verbose_name_plural = "Colectivos"

    def __str__(self):
        return self.name


class SeatCategory(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:

            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["name"]
        verbose_name = "Categoria de Asiento"
        verbose_name_plural = "Categorias de Asiento"

    def __str__(self):
        return self.name


class Seat(models.Model):
    train = models.ForeignKey(Train, related_name="seats", on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    category = models.ForeignKey(
        SeatCategory, related_name="seats", on_delete=models.CASCADE
    )
    is_reserved = models.BooleanField(default=False)

    enabled = models.CharField(
        max_length=1,
        choices=STATES3,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:

            STATES = set(STATES3)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
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
        verbose_name = "Asiento"
        verbose_name_plural = "Asientos"

    def __str__(self):
        return f"{self.seat_number} ({self.category.name})"


class Meal(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    enabled = models.CharField(
        max_length=1,
        choices=STATES2,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Plato"
        verbose_name_plural = "Platos"

    def __str__(self):
        return self.name

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES2)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None


class Merchandise(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Mercaderia"
        verbose_name_plural = "Mercaderias"

    def __str__(self):
        return self.name

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES2)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None


class Journey(models.Model):
    JOURNEY_TYPE_CHOICES = [
        ("TRAIN_ONLY", "Train Only"),
        ("BUS_AND_TRAIN", "Bus and Train"),
    ]

    type = models.CharField(max_length=20, choices=JOURNEY_TYPE_CHOICES)
    description = models.TextField()

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["type"]
        verbose_name = "Recorrido"
        verbose_name_plural = "Recorridos"

    def __str__(self):
        return f"{self.get_type_display()} - {self.description}"


class JourneyStage(models.Model):
    journey = models.ForeignKey(
        Journey, related_name="stages", on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField()
    start_station = models.ForeignKey(
        Station,
        related_name="start_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    end_station = models.ForeignKey(
        Station,
        related_name="end_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start_bus_stop = models.ForeignKey(
        BusStop,
        related_name="start_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    end_bus_stop = models.ForeignKey(
        BusStop,
        related_name="end_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    train = models.ForeignKey(Train, on_delete=models.CASCADE, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField()

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["order"]
        verbose_name = "Etapa de Recorrido"
        verbose_name_plural = "Etapas de Recorrido"

    def __str__(self):
        return f"{self.journey} - Stage {self.order}"


class JourneySchedule(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["journey"]
        verbose_name = "Cronograma de Recorrido"
        verbose_name_plural = "Cronogramas de Recorrido"

    def __str__(self):
        return f"{self.journey} on {self.departure_time}"


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    dni_or_passport = models.CharField(max_length=50)
    origin_country = models.CharField(max_length=100)
    emergency_telephone = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # Telefono (Emergencia)
    # Fecha de Nacimiento
    GENDER = (
        ("m", "Male"),
        ("w", "Female"),
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True,
        default="m",
        help_text="Genero del pasajero",
    )

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["dni_or_passport"]
        verbose_name = "Pasajero"
        verbose_name_plural = "Pasajeros"

    def __str__(self):
        return self.name


class TicketSales(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_date = models.DateTimeField(default=timezone.now)
    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    def update_total_price(self):
        self.price = sum(ticket.price for ticket in self.tickets.all())
        self.save()

    def __str__(self):
        if self.user:
            return f"Sale for {self.user.username} on {self.purchase_date}"
        return f"Sale on {self.purchase_date}"

    class Meta:
        ordering = ["user"]
        verbose_name = "Venta de Boletos"
        verbose_name_plural = "Ventas de Boletos"


class Ticket(models.Model):
    sale = models.ForeignKey(
        TicketSales, related_name="tickets", on_delete=models.CASCADE
    )
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    schedule = models.ForeignKey(JourneySchedule, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ticket for {self.passenger.name} purchased by {self.user.username}"

    # Funcion para reservar el asiento
    def reserveSeat(self):
        asiento = self.seat
        asiento.enabled = "v"
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

        self.reserveSeat()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Cambiar el campo enabled del asiento asociado a 'h' antes de eliminar el ticket
        self.seat.enabled = "h"
        self.seat.save()
        super().delete(*args, **kwargs)

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    def __str__(self):
        return f"Ticket for {self.passenger.name}"

    class Meta:
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"


class PurchaseReceipt(models.Model):
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_date = models.DateTimeField(default=timezone.now)
    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    def update_total_price(self):
        self.price = sum(meal.unit_price * meal.quantity for meal in self.meals.all())
        self.save()

    def update_total_price_of_merchandise(self):
        self.price = sum(
            merchandise.unit_price * merchandise.quantity
            for merchandise in self.merchandises.all()
        )
        self.save()

    def __str__(self):
        if self.passenger:
            return f"Sale for {self.passenger.name} on {self.purchase_date}"
        return f"Sale on {self.purchase_date}"

    class Meta:
        ordering = ["purchase_date"]
        verbose_name = "Factura de Venta"
        verbose_name_plural = "Facturas de Ventas"


class DetailFoodOrder(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt, related_name="meals", on_delete=models.CASCADE
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def delete(self, *args, **kwargs):
        # Cambiar el campo enabled del asiento asociado a 'h' antes de eliminar el ticket
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
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    def __str__(self):
        return f"{self.quantity} x {self.meal.name}"

    class Meta:
        ordering = ["receipt"]
        verbose_name = "Detalle de la Orden de platos"
        verbose_name_plural = "Detalles de la Orden de platos"


class DetailsMerchandiseOrder(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt, related_name="merchandises", on_delete=models.CASCADE
    )
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def delete(self, *args, **kwargs):
        # Cambiar el campo enabled del asiento asociado a 'h' antes de eliminar el ticket
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
            if self.merchandise:
                self.unit_price = self.merchandise.price
                self.update_receipt()

        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = DetailsMerchandiseOrder.objects.get(pk=self.pk)
            if old_instance.merchandise != self.merchandise:
                # Quitar mercaderia del recibo
                self.receipt.price = self.receipt.price - (
                    old_instance.unit_price * old_instance.quantity
                )
                self.unit_price = self.merchandise.price
                self.update_receipt()

        super().save(*args, **kwargs)

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    class Meta:
        ordering = ["receipt"]
        verbose_name = "Detalle de la Orden de mercadería"
        verbose_name_plural = "Detalles de la Orden de mercadería"

    def __str__(self):
        return f"{self.quantity} x {self.merchandise.name}"


class Payments(models.Model):
    sale = models.ForeignKey(
        TicketSales, on_delete=models.CASCADE, null=True, blank=True
    )
    payment_id = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.payment_id and self.payment_type and self.sale:
            return f"Pago {self.payment_id} - {self.payment_type} for - {self.sale}"
        return "Pago" + self.created_at

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
