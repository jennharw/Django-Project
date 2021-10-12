from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
# Create your views here.
import logging, traceback
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Fcuser

def index(request): #root 경로
    db_logger = logging.getLogger('db')
    logging.info('some message')

    db_logger.info('this is register info message') ##user~~
    db_logger.warning('warning message')

    try:
        1/0
    except Exception as e:
        db_logger.exception(e)

    return render(request, 'index.html', {'email': request.session.get('user')})

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'
    
    def form_valid(self, form):
                fcuser = Fcuser(
                    email = form.data.get('email'),
                    password = make_password(form.data.get('password')),
                    level='user'
                )
                fcuser.save()

                return super().form_valid(form)

    val = {'response':'User Added'}
    print("hello user")
    print(JsonResponse(val, status=200))
    logging.info('some message')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    
    return redirect('/')