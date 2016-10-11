from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.db.models import Q

from django import forms
from .models import *
from .forms import StudentForm, Signup_Form, Login_Form
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.utils import timezone


# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request, q_id):
    quiz_test = get_object_or_404(QuizTest, pk=q_id)
    result = {}
    now = timezone.now()
    started = False
    ended = False
    if now > quiz_test.start_date and now < quiz_test.end_date:
        started = True
    elif now > quiz_test.end_date:
        ended = True
    quizquestions = quiz_test.questions.all()
    user = Student.objects.get(user=request.user)
    StudentQuizRelation.objects.get_or_create(student=user, quiztest=quiz_test)
    quiz_relation = quiz_test.studentquizrelation_set.get(student=user)

    # paginator = Paginator(quizquestions_list, 1)
    # end_questions = False
    # page = request.GET.get('page')
    # try:
    #     quizquestions = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     # import ipdb;ipdb.set_trace()
    #     quizquestions = paginator.page(1)
    # except EmptyPage:
    #     end_questions = True
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     quizquestions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        res_dict = json.loads(request.POST['val'])
        for res in res_dict:
            if int(res_dict[res]['question_type']) == 1:
                if 'question_id' in res_dict[res]:
                    quizquestion = QuizQuestion.objects.get(
                        id=res_dict[res]['question_id'])
                    answer_choice = Choice.objects.get(
                        id=res_dict[res]['choice_id'])
                    try:
                        answer_obj = StudentAnswer.objects.get(
                            Q(student_id=user.id) &
                            Q(quiztest_id=quiz_test.id) &
                            Q(question_id=quizquestion.id))
                        answer_obj.answer_choice = answer_choice
                        answer_obj.save()
                    except StudentAnswer.DoesNotExist:
                        studentanswer_obj = StudentAnswer(
                            student=user,
                            quiztest=quiz_test,
                            question=quizquestion,
                            answer_choice=answer_choice)
                        studentanswer_obj.save()
            else:
                if res_dict[res]['text_data']:
                    quizquestion = QuizQuestion.objects.get(
                        id=res_dict[res]['question_id'])
                    answer = res_dict[res]['text_data']
                    try:
                        answer_obj = StudentAnswer.objects.get(
                            Q(student_id=user.id) &
                            Q(quiztest_id=quiz_test.id) &
                            Q(question_id=quizquestion.id))
                        answer_obj.description = answer
                        answer_obj.save()
                    except StudentAnswer.DoesNotExist:
                        studentanswer_obj = StudentAnswer(
                            student=user,
                            quiztest=quiz_test,
                            question=quizquestion,
                            description=answer)
                        studentanswer_obj.save()
        quiz_relation.completed = True
        quiz_relation.save()
    result = {
        'total_questions': quiz_test.questions.all().count(),
        'questions_attempted': quiz_test.studentanswer_set.filter(
            student=user).count()
    }

    return render(
        request, 'quiz/index.html',
        {'quizquestions': quizquestions,
         'user': request.user,
         'quiz_test': quiz_test,
         'quiz_relation': quiz_relation,
         'result': result,
         'now': now,
         'started': started,
         'ended': ended

         }
    )


def signup_form(request):
    if request.method == 'POST':
        print request.POST
        form = Signup_Form(request.POST)
        if form.is_valid():
            user = form.save()
            user_login = authenticate(username=username, password=password)
            if user_login is not None:
                if user_login.is_active:
                    login(request, user_login)
                    return render(
                        request, 'quiz/studentform.html',
                        {'state': state, 'user': user})
    else:
        form = Signup_Form()
    return render(request, 'account/signup.html', {'form': form})


class StudentLoginView(View):

    form_class = StudentForm
    template_name = 'quiz/studentform.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentLoginView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {'form': form, 'user': request.user})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = self.request.user
            student.save()
            quiz = StudentQuizRelation.objects.filter(student=student)
            return render(request, 'quiz/quiz.html', {'quiz': quiz})
        return render(
            request, self.template_name, {'form': form, 'user': request.user})


@login_required(login_url='/accounts/login/')
def Quiz(request):
    if request.user.is_superuser:
        quiz = ''
    else:
        student = Student.objects.get(user=request.user)
        quiz = StudentQuizRelation.objects.filter(
            student=student).order_by('id')

    city = City.objects.all()
    schools = {}
    if request.is_ajax():
        schools = School.objects.filter(city_id=request.POST['city'])
        template = 'quiz/schools.html',
        data = {
            'city': city,
            'schools': schools
        }
        return render(request, template, data)

    return render(
        request, 'quiz/quiz.html',
        {'quiz': quiz, 'city': city, 'user': request.user})


@login_required(login_url='/accounts/login/')
def StudentList(request, s_id):
    school_obj = get_object_or_404(School, pk=s_id)
    students = school_obj.student_set.all()
    return render(request, 'quiz/student_list.html', {'students': students})


@login_required(login_url='/accounts/login/')
def SearchSchool(request):
    city = City.objects.all()
    schools = {}
    if request.is_ajax():
        schools = School.objects.filter(city_id=request.POST['city'])
        template = 'quiz/schools.html',
        data = {
            'city': city,
            'schools': schools
        }
        return render(request, template, data)

    return render(
        request, 'quiz/searchschool.html', {'city': city})


@login_required(login_url='/accounts/login/')
def QuizList(request, s_id):
    student_obj = get_object_or_404(Student, pk=s_id)
    quizzes = student_obj.studentquizrelation_set.filter(
        completed=True).order_by('-id')
    return render(request, 'quiz/student_quizzes.html', {'quizzes': quizzes})


@login_required(login_url='/accounts/login/')
def Results(request, quiz_id, s_id):
    student_obj = get_object_or_404(Student, pk=s_id)
    quiz_test_obj = get_object_or_404(QuizTest, pk=quiz_id)

    answer_obj = StudentAnswer.objects.filter(student=student_obj)
    for question in quiz_test_obj.questions.all():
        if question.question_type == 1:
            student_answer_obj = quiz_test_obj.studentanswer_set.get(
                Q(student=student_obj) &
                Q(question=question))
            try:
                CorrectAnswer.objects.get(
                    correct_choice=student_answer_obj.answer_choice)

                student_answer_obj.result = 1
                student_answer_obj.save()
            except:
                pass
    s = answer_obj.filter(
        Q(quiztest=quiz_test_obj) & Q(result=1)).count()
    relation_obj = quiz_test_obj.studentquizrelation_set.get(
        student=student_obj)
    relation_obj.score = s
    relation_obj.result_published = True
    relation_obj.save()
    correct_count = answer_obj.filter(
        Q(quiztest=quiz_test_obj) &
        Q(result=1)).count()
    attempted_obj = answer_obj.filter(
        Q(student=student_obj) &
        Q(quiztest=quiz_test_obj))
    attempted_count = attempted_obj.count()
    context = {
                'quiz_test_obj': quiz_test_obj,
                'correct_count': correct_count,
                'attempted_count': attempted_count,
                'attempted_obj' : attempted_obj,
                'relation_obj': relation_obj
    }
    return render(request, 'quiz/results.html', context)
