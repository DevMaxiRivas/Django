# Generated by Django 5.0.6 on 2024-05-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0005_alter_libro_portada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(blank=True, help_text='Seleccione una portad', upload_to='portadas/'),
        ),
    ]