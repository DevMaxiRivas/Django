# Generated by Django 5.0.6 on 2024-06-15 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_eventos_pr_ev_alter_ventas_pr_ve'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventos',
            options={'ordering': ['fec_ini_ev'], 'verbose_name': 'Evento'},
        ),
        migrations.AlterModelOptions(
            name='localidades',
            options={'ordering': ['nomb_lc'], 'verbose_name': 'Localidad', 'verbose_name_plural': 'Localidades'},
        ),
        migrations.AlterModelOptions(
            name='lugaresdeevento',
            options={'ordering': ['id_le'], 'verbose_name': 'Lugar de Evento'},
        ),
        migrations.AlterModelOptions(
            name='provincias',
            options={'ordering': ['nomb_pv'], 'verbose_name': 'Provincia'},
        ),
    ]
