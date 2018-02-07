from django import forms
from django.contrib.auth.models import User
from .models import Submission

class SubmitSolForm(forms.Form):
    source = forms.CharField(required=True)
