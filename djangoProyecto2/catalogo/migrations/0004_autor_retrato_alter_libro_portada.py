# Generated by Django 5.0.6 on 2024-05-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_libro_portada'),
    ]

    operations = [
        migrations.AddField(
            model_name='autor',
            name='retrato',
            field=models.ImageField(blank=True, help_text='Seleccione un retrato', upload_to=''),
        ),
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(blank=True, help_text='Seleccione una portada', upload_to=''),
        ),
    ]
