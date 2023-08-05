# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicgroup',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='department',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='faculty',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
