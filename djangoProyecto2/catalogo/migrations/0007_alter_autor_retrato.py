# Generated by Django 5.0.6 on 2024-05-18 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0006_alter_libro_portada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='retrato',
            field=models.ImageField(blank=True, help_text='Seleccione un retrato', upload_to='retratos/'),
        ),
    ]