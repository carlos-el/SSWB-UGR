# Generated by Django 3.0.3 on 2020-04-29 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitas_granada_app', '0009_auto_20200429_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='lat',
            field=models.FloatField(default=37.196459),
        ),
        migrations.AlterField(
            model_name='visita',
            name='lon',
            field=models.FloatField(default=-3.6261883),
        ),
    ]
