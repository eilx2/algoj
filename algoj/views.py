from django.shortcuts import render, HttpResponse
from archive import views
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())


def home(request):
	return render(request,'index.html')

def tutorial(request):
	return render(request,'tutorial.html')

def login(request):
	return render(request,'login.html')

