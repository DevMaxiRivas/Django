# Generated by Django 5.0.6 on 2024-06-18 14:09

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id_ev', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada evento', primary_key=True, serialize=False)),
                ('nomb_ev', models.CharField(max_length=200)),
                ('desc_ev', models.CharField(max_length=200)),
                ('fec_ini_ev', models.DateField(blank=True, null=True)),
                ('fec_fin_ev', models.DateField(blank=True, null=True)),
                ('precio_ev', models.FloatField(blank=True, null=True)),
                ('hab_ev', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado'), ('s', 'Suspendido'), ('f', 'Finalizado')], default='h', max_length=1)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['fec_ini_ev'],
            },
        ),
        migrations.CreateModel(
            name='Localidades',
            fields=[
                ('cod_post_lc', models.CharField(help_text='ID único para cada localidad', max_length=6, primary_key=True, serialize=False)),
                ('nomb_lc', models.CharField(max_length=200)),
                ('hab_lc', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
            ],
            options={
                'verbose_name': 'Localidad',
                'verbose_name_plural': 'Localidades',
                'ordering': ['nomb_lc'],
            },
        ),
        migrations.CreateModel(
            name='Provincias',
            fields=[
                ('id_pv', models.CharField(blank=True, help_text='ID único para cada provincia', max_length=1, primary_key=True, serialize=False)),
                ('nomb_pv', models.CharField(max_length=200)),
                ('hab_pv', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'ordering': ['nomb_pv'],
            },
        ),
        migrations.CreateModel(
            name='LugaresDeEvento',
            fields=[
                ('id_le', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada evento', primary_key=True, serialize=False)),
                ('desc_le', models.CharField(max_length=200)),
                ('tel_le', models.CharField(max_length=15)),
                ('lat_le', models.DecimalField(decimal_places=7, max_digits=10)),
                ('lng_le', models.DecimalField(decimal_places=7, max_digits=10)),
                ('hab_le', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
                ('cod_post_lc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.localidades', verbose_name='Código Postal')),
            ],
            options={
                'verbose_name': 'Lugar de Evento',
                'verbose_name_plural': 'Lugares de Evento',
                'ordering': ['id_le'],
            },
        ),
        migrations.CreateModel(
            name='LugaresDeVenta',
            fields=[
                ('id_lv', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada evento', primary_key=True, serialize=False)),
                ('desc_lv', models.CharField(max_length=200)),
                ('dir_lv', models.CharField(max_length=200)),
                ('tel_lv', models.CharField(max_length=15)),
                ('lat_lv', models.DecimalField(decimal_places=7, max_digits=10)),
                ('lng_lv', models.DecimalField(decimal_places=7, max_digits=10)),
                ('hab_lv', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
                ('cod_post_lc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.localidades', verbose_name='Código Postal')),
            ],
            options={
                'verbose_name': 'Lugar de Venta',
                'verbose_name_plural': 'Lugares de Venta',
                'ordering': ['desc_lv'],
            },
        ),
        migrations.AddField(
            model_name='localidades',
            name='id_pv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.provincias'),
        ),
        migrations.CreateModel(
            name='Secciones',
            fields=[
                ('id_scc', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada seccion por lugar de evento', primary_key=True, serialize=False)),
                ('desc_scc', models.CharField(max_length=200)),
                ('hab_scc', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
                ('id_le', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.lugaresdeevento', verbose_name='Lugar de Evento')),
            ],
            options={
                'verbose_name': 'Sección por Lugar',
                'verbose_name_plural': 'Secciones por Lugar',
                'ordering': ['id_le'],
            },
        ),
        migrations.CreateModel(
            name='EventosPorSeccion',
            fields=[
                ('id_exs', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada evento por seccion', primary_key=True, serialize=False)),
                ('fec_hr_ini_exs', models.DateTimeField(auto_now_add=True)),
                ('fec_hr_fin_exs', models.DateTimeField(auto_now_add=True)),
                ('hab_exs', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado'), ('s', 'Suspendido'), ('f', 'Finalizado')], default='h', max_length=1)),
                ('id_ev', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.eventos', verbose_name='Evento')),
                ('id_scc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.secciones', verbose_name='Seccion')),
            ],
            options={
                'verbose_name': 'Evento por Sección',
                'verbose_name_plural': 'Eventos por Sección',
                'ordering': ['fec_hr_ini_exs'],
            },
        ),
        migrations.CreateModel(
            name='Asientos',
            fields=[
                ('id_as', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada asiento', primary_key=True, serialize=False)),
                ('fila_as', models.CharField(max_length=20)),
                ('column_as', models.CharField(max_length=20)),
                ('hab_as', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado'), ('v', 'Vendido'), ('r', 'Devuelto')], default='h', max_length=1)),
                ('id_scc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.secciones', verbose_name='Seccion')),
            ],
            options={
                'verbose_name': 'Asiento por Sección',
                'verbose_name_plural': 'Asientos por Sección',
                'ordering': ['id_scc'],
            },
        ),
        migrations.CreateModel(
            name='Sectores',
            fields=[
                ('id_sc', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada seccion por lugar de evento', primary_key=True, serialize=False)),
                ('desc_sc', models.CharField(max_length=200)),
                ('filas_sc', models.CharField(help_text='Formato: inicio-final', max_length=20)),
                ('columns_sc', models.CharField(help_text='Formato: inicio-final', max_length=20)),
                ('hab_sc', models.CharField(blank=True, choices=[('h', 'Habilitado'), ('d', 'Desahabilitado')], default='h', max_length=1)),
                ('id_scc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.secciones', verbose_name='Seccion')),
            ],
            options={
                'verbose_name': 'Sector por Sección',
                'verbose_name_plural': 'Sectores por Sección',
                'ordering': ['id_scc'],
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id_ve', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada venta', primary_key=True, serialize=False)),
                ('pr_ve', models.DecimalField(decimal_places=2, max_digits=10)),
                ('as_ve', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.asientos', verbose_name='Asiento')),
                ('cli_ve', models.ForeignKey(limit_choices_to={'groups__name': 'clientes'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('evt_ve', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.eventos', verbose_name='Evento')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['-id_ve'],
            },
        ),
        migrations.CreateModel(
            name='Boletos',
            fields=[
                ('id_bl', models.UUIDField(default=uuid.uuid4, help_text='ID único para cada venta', primary_key=True, serialize=False)),
                ('enVenta_bl', models.BooleanField(default=False)),
                ('cli_bl', models.ForeignKey(limit_choices_to={'groups__name': 'clientes'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('evt_bl', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.eventos', verbose_name='Evento')),
                ('ve_bl', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ventas', verbose_name='Venta')),
            ],
            options={
                'verbose_name': 'Boleto',
                'verbose_name_plural': 'Boletos',
                'ordering': ['-id_bl'],
            },
        ),
    ]