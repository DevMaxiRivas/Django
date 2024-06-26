# Generated by Django 5.0.6 on 2024-06-22 10:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_nationality_passenger_origin_country_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
        migrations.CreateModel(
            name='TicketSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venta de Boletos',
                'verbose_name_plural': 'Ventas de Boletos',
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='sale',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, related_name='sale', to='core.ticketsales'),
            preserve_default=False,
        ),
    ]
