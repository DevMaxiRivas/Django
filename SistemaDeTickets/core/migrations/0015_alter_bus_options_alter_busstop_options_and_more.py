# Generated by Django 5.0.6 on 2024-07-12 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_payments_options_payments_payment_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bus',
            options={'ordering': ['name'], 'verbose_name': 'Bus', 'verbose_name_plural': 'Buses'},
        ),
        migrations.AlterModelOptions(
            name='busstop',
            options={'ordering': ['name'], 'verbose_name': 'Bus stop', 'verbose_name_plural': 'Buses stop'},
        ),
        migrations.AlterModelOptions(
            name='detailfoodorder',
            options={'ordering': ['receipt'], 'verbose_name': 'Detalle de la Orden de platos', 'verbose_name_plural': 'Detail Food Order'},
        ),
        migrations.AlterModelOptions(
            name='detailsmerchandiseorder',
            options={'ordering': ['receipt'], 'verbose_name': 'Food Order Detail', 'verbose_name_plural': 'Food Ordering Details'},
        ),
        migrations.AlterModelOptions(
            name='journey',
            options={'ordering': ['type'], 'verbose_name': 'Journey', 'verbose_name_plural': 'Journeys'},
        ),
        migrations.AlterModelOptions(
            name='journeyschedule',
            options={'ordering': ['journey'], 'verbose_name': 'Journey Schedule', 'verbose_name_plural': 'Journey Schedules'},
        ),
        migrations.AlterModelOptions(
            name='journeystage',
            options={'ordering': ['order'], 'verbose_name': 'Journey Stage', 'verbose_name_plural': 'Journey Stage'},
        ),
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['name'], 'verbose_name': 'Meal', 'verbose_name_plural': 'Meals'},
        ),
        migrations.AlterModelOptions(
            name='merchandise',
            options={'ordering': ['name'], 'verbose_name': 'Merchandise', 'verbose_name_plural': 'Merchandises'},
        ),
        migrations.AlterModelOptions(
            name='passenger',
            options={'ordering': ['dni_or_passport'], 'verbose_name': 'Passenger', 'verbose_name_plural': 'Passengers'},
        ),
        migrations.AlterModelOptions(
            name='payments',
            options={'ordering': ['created_at'], 'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
        migrations.AlterModelOptions(
            name='purchasereceipt',
            options={'ordering': ['purchase_date'], 'verbose_name': 'Purchase Receipt', 'verbose_name_plural': 'Purchase Receipts'},
        ),
        migrations.AlterModelOptions(
            name='seat',
            options={'ordering': ['seat_number'], 'verbose_name': 'Seat', 'verbose_name_plural': 'Seats'},
        ),
        migrations.AlterModelOptions(
            name='seatcategory',
            options={'ordering': ['name'], 'verbose_name': 'Seat Category', 'verbose_name_plural': 'Seat Categories'},
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'ordering': ['name'], 'verbose_name': 'Station', 'verbose_name_plural': 'Stations'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.AlterModelOptions(
            name='ticketsales',
            options={'ordering': ['user'], 'verbose_name': 'Ticket Sale', 'verbose_name_plural': 'Ticket Sales'},
        ),
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ['name'], 'verbose_name': 'Train', 'verbose_name_plural': 'Trains'},
        ),
        migrations.AlterField(
            model_name='bus',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='busstop',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='detailfoodorder',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='detailsmerchandiseorder',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='journey',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='journeyschedule',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='journeystage',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='meal',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled'), ('s', 'Suspended'), ('f', 'Completed')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='merchandise',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='purchasereceipt',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='seat',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled'), ('v', 'Sold'), ('r', 'Returned')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='seatcategory',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='station',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='ticketsales',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
        migrations.AlterField(
            model_name='train',
            name='enabled',
            field=models.CharField(blank=True, choices=[('h', 'Enabled'), ('d', 'Disabled')], default='h', max_length=1),
        ),
    ]