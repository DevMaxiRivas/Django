from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid  # Requerida para las instancias de tuplas únicas


# CURSOS: ESTADOS POSIBLES(STATUS): EN ETAPA DE INSCRIPCION - EN DESARROLLO - FINALIZADO
class Course(models.Model):
    STATUS_CHOICES = (
        ("I", "En etapa de inscripción"),
        ("P", "En progreso"),
        ("F", "Finalizado"),
    )

    name = models.CharField(max_length=90, verbose_name="Nombre")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": "profesores"},
        verbose_name="Profesor",
    )
    class_quantity = models.PositiveIntegerField(
        default=0, verbose_name="Cantidad de clases"
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="I", verbose_name="Estado"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


# INSCRIPCIONES
class Registration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="students_registration",
        limit_choices_to={"groups__name": "estudiantes"},
        verbose_name="Estudiante",
    )
    enabled = models.BooleanField(default=True, verbose_name="Alumno Regular")

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"


# ASISTENCIAS
class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendances",
        limit_choices_to={"groups__name": "estudiantes"},
        verbose_name="Estudiante",
    )
    date = models.DateField(null=True, blank=True, verbose_name="Fecha")
    present = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Presente"
    )

    def __str__(self):
        return f"Asistencia {self.id}"

    # Lógica para generar el estado del alumno regular / irregular (enabled)
    # total-clases => class_quantity del modelo Course
    # total-inasistencias => attendance -> present = False
    # porcentaje-inasistencias = (total-inasistencias / total-clases) * 100 -------> >20 (>20%) => alumno es irregular => enabled = False
    # total-clases = 10
    # total-inasistencias = 4
    # porcentaje-inasistencias = (4 / 10) * 100 = 40 % => seria un alumno irregular

    def update_registration_enabled_status(self):
        course_instance = Course.objects.get(id=self.course.id)
        total_classes = course_instance.class_quantity
        total_absences = Attendance.objects.filter(
            student=self.student, course=self.course, present=False
        ).count()
        absences_percent = (total_absences / total_classes) * 100

        registration = Registration.objects.get(
            course=self.course, student=self.student
        )

        if absences_percent > 20:
            registration.enabled = False
        else:
            registration.enabled = True

        registration.save()

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"


# NOTAS
class Mark(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": "estudiantes"},
        verbose_name="Estudiante",
    )
    mark_1 = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nota 1")
    mark_2 = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nota 2")
    mark_3 = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nota 3")
    average = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True, verbose_name="Promedio"
    )

    def __str__(self):
        return str(self.course)

    # Calcular el promedio (llamo a una función)
    def calculate_average(self):
        marks = [self.mark_1, self.mark_2, self.mark_3]
        valid_marks = [mark for mark in marks if mark is not None]
        if valid_marks:
            return sum(valid_marks) / len(valid_marks)
        return None

    def save(self, *args, **kwargs):
        # Verifico si alguna nota cambio
        if self.mark_1 or self.mark_2 or self.mark_3:
            self.average = (
                self.calculate_average()
            )  # Calcular el promedio (llamo a una función)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"


class Provincias(models.Model):
    id_pv = models.CharField(
        primary_key=True,
        max_length=200,
        help_text="ID único para cada provincia",
    )
    nomb_pv = models.CharField(max_length=200)

    ESTADOS_TUPLA = (
        ("h", "Habilitado"),
        ("d", "Desahabilitado"),
    )

    hab_pv = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["nomb_pv"]
        verbose_name = "Provincia"

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

    ESTADOS_TUPLA = (
        ("h", "Habilitado"),
        ("d", "Desahabilitado"),
    )

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
    pr_ev = models.DecimalField(max_digits=10, decimal_places=2)

    ESTADOS_TUPLA = (
        ("h", "Habilitado"),
        ("d", "Desahabilitado"),
        ("s", "Suspendido"),
        ("f", "Finalizado"),
        ("a", "Actualizado"),
    )

    hab_ev = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["fec_ini_ev"]
        verbose_name = "Evento"

    def __str__(self):
        return "%s (%s)" % (self.nomb_ev, self.desc_ev)

    def muestra_estado(self):
        if self.hab_ev:
            # Convierto a diccionaria el valor estado ejemplar
            ESTADOS_TUPLA = {
                ("h", "Habilitado"),
                ("d", "Desahabilitado"),
                ("s", "Suspendido"),
                ("f", "Finalizado"),
                ("a", "Actualizado"),
            }
            # Retornar el valor correspondiente
            return ESTADOS_TUPLA.get(self.estado)
        return None

    # Funcion para actualizar el estado de los boletos si es que se actualiza el evento (No necesario, usado para pruebas)
    def seActualizo(self):
        boletos = Boletos.objects.filter(evt_bl=self)
        for boleto in boletos:
            if not boleto.enVenta_bl:
                boleto.enVenta_bl = True
                boleto.save()


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

    cod_post_lc = models.ForeignKey(Localidades, on_delete=models.CASCADE, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.

    ESTADOS_TUPLA = (
        ("h", "Habilitado"),
        ("d", "Desahabilitado"),
        ("s", "Suspendido"),
        ("f", "Finalizado"),
    )

    hab_ev = models.CharField(
        max_length=1,
        choices=ESTADOS_TUPLA,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["id_le"]
        verbose_name = "Lugar de Evento"

    def __str__(self):
        return "%s (%s)" % (self.id_le, self.desc_le)


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
    pr_ve = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Si es el mismo evento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.evt_ve:
                self.pr_ve = self.evt_ve.pr_ev
        # Sino es el mismo evento con el que se creo la venta modificar el precio de la venta al precio del evento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = Ventas.objects.get(pk=self.pk)
            if old_instance.evt_ve != self.evt_ve:
                self.pr_ve = self.evt_ve.pr_ev
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


@receiver(post_save, sender=Attendance)
@receiver(post_delete, sender=Attendance)
def update_registration_enabled_status(sender, instance, **kwargs):
    instance.update_registration_enabled_status()


@receiver(post_save, sender=Eventos)
@receiver(post_delete, sender=Eventos)
def update_an_event(sender, instance, **kwargs):
    instance.seActualizo()
