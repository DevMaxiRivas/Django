# Generated by Django 5.0.6 on 2024-06-15 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provincias',
            name='id_pv',
            field=models.CharField(help_text='ID único para cada provincia', max_length=200, primary_key=True, serialize=False),
        ),
    ]