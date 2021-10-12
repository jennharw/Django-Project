"""fc_django2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from fcuser.views import RegisterView, LoginView
from django.contrib import admin
from django.urls import path, include
from fcuser.views import index, logout
from product.views import ProductList, ProductCreate, ProductDetail, ProductListApi, ProductDetailApi
from order.views import OrderCreate, OrderList
from django.views.generic import TemplateView
from order.models import Order
import datetime

#view (data) -> html ; app , site 
#admin.site. admin.site.index
#data 함수로 끼워넣기 
orig_index = admin.site.index

def fastcampus_index(request, extra_context=None):
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
   # extra_context = {'labels':'', 'data':'['test1', 'test2', 'test3']', 'test':'test1'}
   # {'orders' : {key : value, ..} , 'test':'test1'}
    order_data = {}
    for i in range(7):
        target_dttm = base_date + datetime.timedelta(days=i)
        #date_key = target_dttm.strftime('%Y-%m-%d')
        target_date = datetime.date(target_dttm.year, target_dttm.month, target_dttm.day)
        order_cnt = Order.objects.filter(register_date__date = target_date).count()
        order_data[target_date] = order_cnt

    extra_context = {'test':'test1', 'orders':order_data}

    return orig_index(request, extra_context)

admin.site.index = fastcampus_index

urlpatterns = [
    path('admin/manual', TemplateView.as_view(template_name='admin/manual.html', extra_context={'title':'매뉴얼', 'site_title':'패스트캠퍼스'})),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('', index),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('product/', ProductList.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),
    path('logout/', logout),
    path('api/product/', ProductListApi.as_view()),
    path('api/product/<int:pk>/', ProductDetailApi.as_view())



]
