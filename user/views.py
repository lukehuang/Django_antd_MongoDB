from django.shortcuts import render,HttpResponse
from bottle import request
# from .models import UserCount
from django.views.generic import View

# Create your views here.

class User(View):
    def get(self,request):

        return render(request, 'user/index.html')