# Generated by Django 5.1.6 on 2025-04-08 05:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objetivos_especificos', '0001_initial'),
        ('temas', '0002_temas_sub_temas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objetivos_especificos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competencias', to='objetivos_especificos.objetivosespecificos')),
                ('temas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competencias', to='temas.temas')),
            ],
        ),
    ]
