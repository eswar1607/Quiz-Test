# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 07:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CorrectAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('correct_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='QuizInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invited', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('question_type', models.IntegerField(choices=[(1, 'multiple'), (2, 'essay')])),
            ],
        ),
        migrations.CreateModel(
            name='QuizTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('questions', models.ManyToManyField(to='quiz.QuizQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.City')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.IntegerField()),
                ('standard', models.CharField(max_length=200)),
                ('joining', models.DateField(blank=True, null=True)),
                ('ending', models.DateField(blank=True, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.School')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('result', models.IntegerField(blank=True, choices=[(1, 'correct'), (2, 'wrong')], null=True)),
                ('answer_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizQuestion')),
                ('quiztest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizTest')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentQuizRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, null=True)),
                ('certificate', models.CharField(blank=True, max_length=500, null=True)),
                ('quiztest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizTest')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Student')),
            ],
        ),
        migrations.AddField(
            model_name='quizinvitation',
            name='quiztest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizTest'),
        ),
        migrations.AddField(
            model_name='quizinvitation',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.School'),
        ),
        migrations.AddField(
            model_name='correctanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizQuestion'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizQuestion'),
        ),
    ]
