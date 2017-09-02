# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-31 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attractions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('text', models.TextField(default='', max_length=1000)),
                ('wikipedia', models.URLField(blank=True)),
                ('tripadvisor', models.URLField(blank=True)),
                ('google_map', models.URLField(blank=True)),
                ('web_site', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
