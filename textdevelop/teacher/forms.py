from django import forms
from .models import Teacher

class RecommendForm(forms.Form):
    recommendWord = forms.CharField(
        error_messages={
            'required' : '문장을 입력하시오'
        },
        max_length=256, label = "추천 문장")
   
    def clean(self):
        cleaned_data = super().clean()
        recommendWord = cleaned_data.get('recommendWord')
        