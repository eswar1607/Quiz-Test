from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms import DateTimeField


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ["user"]

    def clean_roll_number(self):
        number = self.cleaned_data.get('roll_number')
        if Student.objects.filter(roll_number=number).exists():
            raise forms.ValidationError('This rollnumber already exists')
        return number


class Login_Form(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        name = self.cleaned_data.get('Name')
        if User_detail.objects.filter(Name = name).exists():
            raise forms.ValidationError('This username already exists')
        return name




class Signup_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 're_password']

    def save(self):
        user = super(Signup_Form, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    def clean(self):
        if 'password' in self.cleaned_data and 're_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['re_password']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data
