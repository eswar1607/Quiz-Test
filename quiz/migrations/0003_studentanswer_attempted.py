# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_studentquizrelation_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
    ]
