# Generated by Django 5.0.6 on 2024-06-15 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_provincias_id_pv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='id_ev',
            field=models.CharField(help_text='ID único para cada evento', max_length=6, primary_key=True, serialize=False),
        ),
    ]
