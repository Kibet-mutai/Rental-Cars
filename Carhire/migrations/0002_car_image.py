# Generated by Django 4.1.1 on 2022-10-25 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Carhire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
