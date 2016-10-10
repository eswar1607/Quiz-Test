from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(City),
admin.site.register(QuizQuestion),
admin.site.register(Choice),
admin.site.register(School),
admin.site.register(QuizTest),
admin.site.register(QuizInvitation),
admin.site.register(CorrectAnswer),
admin.site.register(Student),
admin.site.register(StudentAnswer),
admin.site.register(StudentQuizRelation),


