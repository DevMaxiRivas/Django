# Generated by Django 5.0.6 on 2024-06-15 22:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_eventos_id_ev'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='id_ev',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID único para cada evento', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='localidades',
            name='cod_post_lc',
            field=models.CharField(help_text='ID único para cada localidad', max_length=6, primary_key=True, serialize=False),
        ),
    ]
