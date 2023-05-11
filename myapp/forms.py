from django.forms import ModelForm
from . models import student
from django import forms
class StudentForm (ModelForm):
    class Meta:
        model=student
        fields ='__all__'
   
        