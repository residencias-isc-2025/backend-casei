# Generated by Django 5.1.6 on 2025-04-25 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienciaProfesionalNoAcademica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad_puesto', models.CharField(max_length=255)),
                ('organizacion_empresa', models.CharField(max_length=255)),
                ('d_mes_anio', models.DateField()),
                ('a_mes_anio', models.DateField()),
            ],
        ),
    ]
