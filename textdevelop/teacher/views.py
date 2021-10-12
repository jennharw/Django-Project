from django.http.request import QueryDict
from django.shortcuts import render
from .models import Teacher
# Create your views here.
from django.shortcuts import render, redirect
from .forms import RecommendForm
from django.views.generic.edit import FormView

import sys
sys.path.append('C://Users/user/OneDrive - 고려대학교/바탕 화면/21연구과제/연구21_2/KL/VGCN_BERT')

#from classify_03 import Classify03
from classify_03 import Classify03



class RecommendView(FormView):
    template_name = 'recommend.html'
    form_class = RecommendForm
    success_url = 'admin/'
    def form_valid(self, form):
        recommend_word = form.data.get('recommendWord')
        print(form.data.get('recommendWord'))

        recommendTeacher = Classify03(recommend_word)
        print("--------------")
        print(recommendTeacher.recommend())



        return super().form_valid(form)

        