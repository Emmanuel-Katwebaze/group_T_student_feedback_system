from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Student, Instructor


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email',
                  'course', 'enrollment_year', 'password')

#validation of the questions for proper formatting 
class QuestionForm(forms.Form):
    question = forms.CharField(max_length=255)
    question_type = forms.ChoiceField(choices=[('text', 'Paragraph'), ('multipleChoice', 'Multiple Choice')])
    options = forms.CharField(max_length=1000, required=False)



    
