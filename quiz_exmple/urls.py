"""quiz_exmple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from quiz import views
from quiz.views import *
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/login/$', views.login_form, name='login_form'),
    url(r'^accounts/signup/$', views.signup_form, name='signup_form'),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^accounts/profile/$',
     StudentLoginView.as_view(), name='account_profile'),
    url(r'^$', TemplateView.as_view(template_name="quiz/home.html"), name="home"),

]