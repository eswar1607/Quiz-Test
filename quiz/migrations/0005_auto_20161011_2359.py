# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20161009_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztest',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quiztest',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]