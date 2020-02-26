# Generated by Django 3.0.3 on 2020-02-16 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripción', models.CharField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=500)),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitas_granada_app.Visita')),
            ],
        ),
    ]
