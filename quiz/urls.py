from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    url(r'^(?P<q_id>[0-9]+)/$', views.index, name='index'),
    url(r'^quizzes/$', views.Quiz, name='quizzes'),
    url(r'^schools/(?P<s_id>[0-9]+)/$', views.StudentList, name='student_list'),
    url(r'^searchschool/$', views.SearchSchool, name='SearchSchool'),
    url(r'^students/quizzes/(?P<s_id>[0-9]+)/$', views.QuizList, name='quiz_list'),
    url(r'^(?P<quiz_id>[0-9]+)/student/(?P<s_id>[0-9]+)/$', views.Results, name='results'),




    # url(r'^student/$', StudentLoginView.as_view(), name='studentlogin'),
    # url(r'^savedata/$', views.AnswerSaving, name='AnswerSaving'),
]
