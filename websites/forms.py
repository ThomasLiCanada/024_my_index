# websites/forms.py

from django import forms
from .models import *


class InputIndexForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = ['key_words',
                  'address',
                  'category1',
                  ]


class InputIndexCategoryForm(forms.ModelForm):
    class Meta:
        model = IndexCategory
        fields = '__all__'


class ToDoTaskForm(forms.ModelForm):
    class Meta:
        model = ToDoTask
        fields = '__all__'
