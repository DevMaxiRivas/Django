# Generated by Django 5.0.6 on 2024-06-15 23:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_eventos_id_ev_alter_localidades_cod_post_lc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Venta',
            new_name='Ventas',
        ),
    ]
