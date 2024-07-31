# Generated by Django 5.0.6 on 2024-07-20 00:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_rename_categories_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
            ],
            options={
                'verbose_name': 'Plato',
                'verbose_name_plural': 'Platos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SeatCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=100, null=True, verbose_name='type')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
            ],
            options={
                'verbose_name': 'Categoria de Asiento',
                'verbose_name_plural': 'Categorias de Asiento',
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='Stops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('location', models.CharField(max_length=255, verbose_name='location')),
                ('type', models.CharField(blank=True, choices=[('b', 'Bus'), ('t', 'Train')], default='t', max_length=1, verbose_name='type')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
            ],
            options={
                'verbose_name': 'Parada',
                'verbose_name_plural': 'Paradas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
            ],
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price'),
        ),
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('capacity', models.PositiveIntegerField(blank=True, null=True, verbose_name='capacity')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.transport', verbose_name='transport')),
            ],
            options={
                'verbose_name': 'Tren',
                'verbose_name_plural': 'Trenes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=10, verbose_name='seat_number')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='dashboard.seatcategory', verbose_name='category')),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='dashboard.transport', verbose_name='transport')),
            ],
            options={
                'verbose_name': 'Asiento',
                'verbose_name_plural': 'Asientos',
                'ordering': ['seat_number'],
            },
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('capacity', models.PositiveIntegerField(blank=True, null=True, verbose_name='capacity')),
                ('enabled', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Deshabilitado')], default='h', max_length=1, verbose_name='enabled')),
                ('transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.transport', verbose_name='transport')),
            ],
            options={
                'verbose_name': 'Colectivo',
                'verbose_name_plural': 'Colectivos',
                'ordering': ['name'],
            },
        ),
    ]