# Generated by Django 5.0.6 on 2024-05-30 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0007_alter_autor_retrato'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'ordering': ['apellido', 'nombre']},
        ),
        migrations.AddField(
            model_name='autor',
            name='foto',
            field=models.ImageField(null=True, upload_to='catalogo/upload/img/'),
        ),
        migrations.AlterField(
            model_name='autor',
            name='retrato',
            field=models.ImageField(blank=True, upload_to='retratos/'),
        ),
    ]
