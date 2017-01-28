# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-25 14:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaComentario', models.DateTimeField(auto_now_add=True)),
                ('autor', models.CharField(default='anonimo', max_length=100)),
                ('cuerpoComentario', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('cuerpo', models.TextField()),
                ('fecha', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='entrada',
            name='etiqueta',
            field=models.ManyToManyField(blank=True, to='Blog.Etiqueta'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='idEntrada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog.Entrada'),
        ),
    ]