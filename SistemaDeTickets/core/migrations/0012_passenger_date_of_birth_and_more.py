# Generated by Django 5.0.6 on 2024-07-02 13:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_purchasereceipt_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='passenger',
            name='emergency_telephone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detailfoodorder',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='core.purchasereceipt'),
        ),
    ]