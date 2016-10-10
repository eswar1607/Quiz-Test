from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class City(models.Model):

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.name


class School(models.Model):

    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s" % self.name


class QuizQuestion(models.Model):

    MULTIPLE = 1
    ESSAY = 2

    QUESTION_TYPE_CHOICES = (
        (MULTIPLE, 'multiple'),
        (ESSAY, 'essay'),
    )
    question = models.CharField(max_length=200)
    question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES)

    def __unicode__(self):
        return u"%s" % self.question


class QuizTest(models.Model):

    title = models.CharField(max_length=200)
    questions = models.ManyToManyField(QuizQuestion)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % self.title


class QuizInvitation(models.Model):

    quiztest = models.ForeignKey(QuizTest, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    invited = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.quiztest.title


class Choice(models.Model):

    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.choice, self.question.question)


class CorrectAnswer(models.Model):

    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    correct_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.question.question


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    standard = models.CharField(max_length=200)
    joining = models.DateField(null=True, blank=True)
    ending = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.user.username


class StudentAnswer(models.Model):

    CORRECT = 1
    WRONG = 2

    STUDENT_RESULT_CHOICES = (
        (CORRECT, 'correct'),
        (WRONG, 'wrong'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiztest = models.ForeignKey(QuizTest, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    result = models.IntegerField(default=2,
        choices=STUDENT_RESULT_CHOICES, null=True, blank=True)
    attempted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.student.user.username


class StudentQuizRelation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiztest = models.ForeignKey(QuizTest, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    certificate = models.CharField(max_length=500, null=True, blank=True)
    completed = models.BooleanField(default=False)
    result_published = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s  %s " % (self.quiztest.title, self.student.user.username)
