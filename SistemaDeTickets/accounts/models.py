from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Traducciones
from django.utils.translation import gettext as _


# PERFIL DE USUARIO
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="Usuario"
    )
    image = models.ImageField(
        default="users/default.png",
        upload_to="users/",
        verbose_name="Imagen de perfil",
    )
    address = models.CharField(
        max_length=150, null=True, blank=True, verbose_name="Dirección"
    )
    location = models.CharField(
        max_length=150, null=True, blank=True, verbose_name="Localidad"
    )
    telephone = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Teléfono"
    )

    class Meta:
        verbose_name = _("perfil")
        verbose_name_plural = _("perfiles")
        ordering = ["-id"]

    def __str__(self):
        return self.user.username


# Con esto cuando se crea un usuario => se crea un perfil con un grupo predeterminado "cliente"
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Cuando se cree un perfil que impacte en la base de datos
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
