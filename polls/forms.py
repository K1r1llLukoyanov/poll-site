from .models import Question, Choice, Category
from django import forms


class CreateQuestionForm(forms.Form):
    question_text = forms.CharField(label="Question text", max_length=300)


class CreateChoiceForm(forms.Form):
    choice_text = forms.CharField(label="Choice text", max_length=150)
    id = 0


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'img']