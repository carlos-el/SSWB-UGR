# Generated by Django 3.0.3 on 2020-02-16 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitas_granada_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visita',
            old_name='descripción',
            new_name='descripcion',
        ),
    ]
