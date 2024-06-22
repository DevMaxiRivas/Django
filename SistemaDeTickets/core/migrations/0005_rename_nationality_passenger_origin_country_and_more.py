# Generated by Django 5.0.6 on 2024-06-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_price_multiplier_seatcategory_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='nationality',
            new_name='origin_country',
        ),
        migrations.AlterField(
            model_name='passenger',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('w', 'Female')], default='m', help_text='Genero del pasajero', max_length=1),
        ),
    ]
