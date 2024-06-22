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
        verbose_name = "Parada de autobus"
        verbose_name_plural = "Paradas de autobus"

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
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2)

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
    #         # Si es el mismo evento con el que se creo la venta no modificar el precio
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


class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule = models.ForeignKey(JourneySchedule, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    enabled = models.CharField(
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    # Funcion para reservar el asiento
    def reservarAsiento(self):
        asiento = Seat.objects.filter(pk=self.seat.pk)
        asiento.hab_as = "v"
        asiento.save()

    # def save(self, *args, **kwargs):
    #     # Si es el mismo evento con el que se creo la venta no modificar el precio
    #     if self._state.adding:
    #         if self.evt_ve:
    #             self.pr_ve = self.evt_ve.precio_ev
    #     # Sino es el mismo evento con el que se creo la venta modificar el precio de la venta al precio del evento nuevo seleccionado.
    #     else:
    #         # Si el objeto ya existe en la base de datos
    #         old_instance = Ticket.objects.get(pk=self.pk)
    #         if old_instance.evt_ve != self.evt_ve:
    #             self.pr_ve = self.evt_ve.precio_ev

    #     self.reservarAsiento(self)
    #     super().save(*args, **kwargs)

    def status_sample(self):
        if self.enabled:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.enabled)
        return None

    def __str__(self):
        return f"Ticket for {self.user.username} on {self.schedule}"

    class Meta:
        ordering = ["purchase_date"]
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"


class MealOrder(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name="meal_orders", on_delete=models.CASCADE
    )
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
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

    def __str__(self):
        return f"{self.quantity} x {self.meal.name} for {self.ticket.user.username}"

    class Meta:
        ordering = ["ticket"]
        verbose_name = "Orden de plato"
        verbose_name_plural = "Ordenes de platos"


class MerchandiseOrder(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name="merchandise_orders", on_delete=models.CASCADE
    )
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

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
        ordering = ["ticket"]
        verbose_name = "Orden de mercadería"
        verbose_name_plural = "Ordenes de mercadería"

    def __str__(self):
        return (
            f"{self.quantity} x {self.merchandise.name} for {self.ticket.user.username}"
        )


# @receiver(post_save, sender=Ventas)
# @receiver(post_delete, sender=Ventas)
# def update_an_sale(sender, instance, **kwargs):
#     instance.reservarAsiento()
