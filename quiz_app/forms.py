from django import forms
from .models import Question, Choice

class NameForm(forms.Form):
    name = forms.CharField(label='Ism Familiyangizni kiriting. . .', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': 'name'}
    ), required=True)



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']
