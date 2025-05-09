# Generated by Django 5.1.6 on 2025-04-25 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('indicador_alcance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NivelDesempenio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('valor', models.FloatField()),
                ('indicador_alcance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveles', to='indicador_alcance.indicadoralcance')),
            ],
        ),
    ]
