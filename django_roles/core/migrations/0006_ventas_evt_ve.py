# Generated by Django 5.0.6 on 2024-06-15 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_venta_ventas'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='evt_ve',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.eventos', verbose_name='Evento'),
        ),
    ]
