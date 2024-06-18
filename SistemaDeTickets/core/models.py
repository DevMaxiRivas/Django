from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid  # Requerida para las instancias de tuplas únicas


ESTADOS_TUPLA = (
    ("h", "Habilitado"),
    ("d", "Desahabilitado"),
)

ESTADOS_TUPLA2 = (
    ("h", "Habilitado"),
    ("d", "Desahabilitado"),
    ("s", "Suspendido"),
    ("f", "Finalizado"),
)

ESTADOS_TUPLA3 = (
    ("h", "Habilitado"),
    ("d", "Desahabilitado"),
    ("v", "Vendido"),
    ("r", "Devuelto"),
)

class Provincias(models.Model):
    id_pv  = models.CharField(
        primary_key=True,
        max_length=1,
        blank=True,
        help_text="ID único para cada provincia",
    )
    nomb_pv = models.CharField(max_length=200)

    hab_pv = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["nomb_pv"]
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
    
    def muestra_estado(self):
        if self.hab_pv:
            ESTADOS = set(ESTADOS_TUPLA)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_pv)
        return None

    def __str__(self):
        return "%s (%s)" % (self.id_pv, self.nomb_pv)


class Localidades(models.Model):
    cod_post_lc = models.CharField(
        primary_key=True,
        max_length=6,
        help_text="ID único para cada localidad",
    )
    nomb_lc = models.CharField(max_length=200)
    id_pv = models.ForeignKey(Provincias, on_delete=models.CASCADE, null=True)


    hab_lc = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["nomb_lc"]
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"

    def __str__(self):
        return "%s (%s)" % (self.cod_post_lc, self.nomb_lc)
    
class LugaresDeVenta(models.Model):
    id_lv = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada evento",
    )
    desc_lv = models.CharField(max_length=200)
    dir_lv = models.CharField(max_length=200)
    tel_lv = models.CharField(max_length=15)
    lat_lv = models.DecimalField(max_digits=10, decimal_places=7)
    lng_lv = models.DecimalField(max_digits=10, decimal_places=7)
    cod_post_lc = models.ForeignKey(
        Localidades,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Código Postal",
    )

    hab_lv = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["desc_lv"]
        verbose_name = "Lugar de Venta"
        verbose_name_plural = "Lugares de Venta"

    def __str__(self):
        return "%s (%s)" % (self.desc_lv, self.dir_lv)

    def muestra_estado(self):
        if self.hab_lv:
            ESTADOS = set(ESTADOS_TUPLA)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_lv)
        return None

class LugaresDeEvento(models.Model):
    id_le = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada evento",
    )
    desc_le = models.CharField(max_length=200)
    tel_le = models.CharField(max_length=15)
    lat_le = models.DecimalField(max_digits=10, decimal_places=7)
    lng_le = models.DecimalField(max_digits=10, decimal_places=7)
    cod_post_lc = models.ForeignKey(Localidades, on_delete=models.CASCADE, null=True, verbose_name="Código Postal")
    

    hab_le = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )
    
    def muestra_estado(self):
        if self.hab_le:
            ESTADOS = set(ESTADOS_TUPLA)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_le)
        return None

    class Meta:
        ordering = ["id_le"]
        verbose_name = "Lugar de Evento"
        verbose_name_plural = "Lugares de Evento"

    def __str__(self):
        return "%s" % (self.desc_le)


class Secciones(models.Model):
    id_scc = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada seccion por lugar de evento",
    )
    desc_scc = models.CharField(max_length=200)
    id_le = models.ForeignKey(LugaresDeEvento, on_delete=models.CASCADE, null=True, verbose_name="Lugar de Evento")
    

    hab_scc = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )
    
    def muestra_estado(self):
        if self.hab_scc:

            ESTADOS = set(ESTADOS_TUPLA)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_scc)
        return None

    class Meta:
        ordering = ["id_le"]
        verbose_name = "Sección por Lugar"
        verbose_name_plural = "Secciones por Lugar"

    def __str__(self):
        return "%s (%s)" % (self.desc_scc, self.id_le.desc_le)
    
class Sectores(models.Model):
    id_sc = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada seccion por lugar de evento",
    )
    desc_sc = models.CharField(max_length=200)
    id_scc = models.ForeignKey(Secciones, on_delete=models.CASCADE, null=True, verbose_name="Seccion")
    
    filas_sc = models.CharField(max_length=20, help_text="Formato: inicio-final")
    columns_sc = models.CharField(max_length=20, help_text="Formato: inicio-final")
    hab_sc = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )
    
    def muestra_estado(self):
        if self.hab_sc:

            ESTADOS = set(ESTADOS_TUPLA)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_sc)
        return None

    class Meta:
        ordering = ["id_scc"]
        verbose_name = "Sector por Sección"
        verbose_name_plural = "Sectores por Sección"

    def __str__(self):
        return "%s (%s)" % (self.desc_sc, self.id_scc.desc_scc)
    
class Asientos(models.Model):
    id_as = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada asiento",
    )
    fila_as = models.CharField(max_length=20)
    column_as = models.CharField(max_length=20)
    id_scc = models.ForeignKey(Secciones, on_delete=models.CASCADE, null=True, verbose_name="Seccion")
    
    hab_as = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA3,
        blank=True,
        default="h",
    )
    
    def muestra_estado(self):
        if self.hab_as:

            ESTADOS = set(ESTADOS_TUPLA3)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_as)
        return None

    class Meta:
        ordering = ["id_scc"]
        verbose_name = "Asiento por Sección"
        verbose_name_plural = "Asientos por Sección"

    def __str__(self):
        return "Asiento (%s %s)" % (self.fila_as, self.column_as)



class Eventos(models.Model):
    id_ev = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada evento",
    )
    nomb_ev = models.CharField(max_length=200)
    desc_ev = models.CharField(max_length=200)
    fec_ini_ev = models.DateField(null=True, blank=True)
    fec_fin_ev = models.DateField(null=True, blank=True)
    precio_ev = models.FloatField(null=True, blank=True)

    hab_ev = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA2,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["fec_ini_ev"]
        verbose_name = "Evento"
        verbose_name_plural	 = "Eventos"

    def __str__(self):
        return "%s (%s)" % (self.nomb_ev, self.desc_ev)

    def muestra_estado(self):
        if self.hab_ev:
            ESTADOS = set(ESTADOS_TUPLA2)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_ev)
        return None

class EventosPorSeccion(models.Model):
    id_exs = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada evento por seccion",
    )
    fec_hr_ini_exs = models.DateTimeField(auto_now_add=True)
    fec_hr_fin_exs = models.DateTimeField(auto_now_add=True)
    id_scc = models.ForeignKey(Secciones, on_delete=models.CASCADE, null=True, verbose_name="Seccion")
    id_ev = models.ForeignKey(Eventos, on_delete=models.CASCADE, null=True, verbose_name="Evento")
    
    hab_exs = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA2,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["fec_hr_ini_exs"]
        verbose_name = "Evento por Sección"
        verbose_name_plural	 = "Eventos por Sección"

    def __str__(self):
        return "%s (%s)" % (self.id_ev.desc_ev, self.id_scc.desc_scc)

    def muestra_estado(self):
        if self.hab_exs:
            ESTADOS = set(ESTADOS_TUPLA2)
            # Retornar el valor correspondiente
            return ESTADOS.get(self.hab_exs)
        return None


class Ventas(models.Model):
    id_ve = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada venta",
    )
    cli_ve = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        # Con esto limitamos a que se puedan agregar solo clientes
        limit_choices_to={"groups__name": "clientes"},
        verbose_name="Cliente",
    )
    evt_ve = models.ForeignKey(
        Eventos,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Evento",
    )
    as_ve = models.ForeignKey(
        Asientos,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Asiento",
    )
    pr_ve = models.DecimalField(max_digits=10, decimal_places=2)

    # Funcion para reservar el asiento
    def reservarAsiento(self):
        asiento = Asientos.objects.filter(pk=self.as_ve.pk)
        asiento.hab_as = "v"
        asiento.save()
        

    def save(self, *args, **kwargs):
        # Si es el mismo evento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.evt_ve:
                self.pr_ve = self.evt_ve.precio_ev
        # Sino es el mismo evento con el que se creo la venta modificar el precio de la venta al precio del evento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = Ventas.objects.get(pk=self.pk)
            if old_instance.evt_ve != self.evt_ve:
                self.pr_ve = self.evt_ve.precio_ev
                
        self.reservarAsiento(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s (%s)" % (self.id_ve, self.pr_ve)

    class Meta:
        ordering = ["-id_ve"]
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class Boletos(models.Model):
    id_bl = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="ID único para cada venta",
    )
    cli_bl = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        # Con esto limitamos a que se puedan agregar solo clientes
        limit_choices_to={"groups__name": "clientes"},
        verbose_name="Cliente",
    )
    evt_bl = models.ForeignKey(
        Eventos,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Evento",
    )
    ve_bl = models.ForeignKey(
        Ventas,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Venta",
    )
    enVenta_bl = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si es el mismo evento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.ve_bl:
                self.cli_bl = self.ve_bl.cli_ve
                self.evt_bl = self.ve_bl.evt_ve

        super().save(*args, **kwargs)

    def __str__(self):
        return "%s (%s)" % (self.cli_bl, self.evt_bl)

    class Meta:
        ordering = ["-id_bl"]
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"


@receiver(post_save, sender=Ventas)
@receiver(post_delete, sender=Ventas)
def update_an_sale(sender, instance, **kwargs):
    instance.reservarAsiento()
