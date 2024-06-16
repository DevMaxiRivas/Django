from django.contrib.auth.models import Group

# Herramienta para manejar señales (signals)
from django.dispatch import receiver

from django.db.models.signals import post_save
from .models import Profile

# Archivo que actua cuando recibe la grabacion de un usuario
# este lo asigna a un grupo


@receiver(post_save, sender=Profile)
def add_user_to_students_group(sender, instance, created, **kwargs):
    # Verificamos si existe el grupo estudiante
    if created:
        try:
            group1 = Group.objects.get(name="estudiantes")
        # Si no existe
        except Group.DoesNotExist:
            group1 = Group.objects.create(name="estudiantes")
            group2 = Group.objects.create(name="profesores")
            group3 = Group.objects.create(name="preceptores")
            group4 = Group.objects.create(name="administrativos")
            group5 = Group.objects.create(name="clientes")
            group6 = Group.objects.create(name="vendedores")
            group7 = Group.objects.create(name="dbas")
        instance.user.groups.add(group1)
