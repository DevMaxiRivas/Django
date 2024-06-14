from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if (
        sender.name == "venta"
    ):  # Asegúrate de que esto solo se ejecute para la aplicación 'venta'
        editors_group, created = Group.objects.get_or_create(name="Editors")
        if created:
            can_edit_permission = Permission.objects.get(codename="can_edit")
            editors_group.permissions.add(can_edit_permission)

        publishers_group, created = Group.objects.get_or_create(name="Publishers")
        if created:
            can_publish_permission = Permission.objects.get(codename="can_publish")
            publishers_group.permissions.add(can_publish_permission)
