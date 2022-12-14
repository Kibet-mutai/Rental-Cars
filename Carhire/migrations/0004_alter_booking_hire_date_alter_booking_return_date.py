# Generated by Django 4.1.1 on 2022-10-26 08:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Carhire', '0003_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='hire_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='return_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
