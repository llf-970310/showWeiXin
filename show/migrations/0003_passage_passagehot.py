# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0002_keyword_releate'),
    ]

    operations = [
        migrations.AddField(
            model_name='passage',
            name='passagehot',
            field=models.FloatField(default=0, verbose_name='热度'),
        ),
    ]
