# Generated by Django 5.0.6 on 2024-06-22 12:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_ticket_options_remove_ticket_purchase_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasereceipt',
            name='purchase_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='purchasereceipt',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ticketsales',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]