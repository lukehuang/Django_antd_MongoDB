from django.shortcuts import render,HttpResponse,HttpResponseRedirect
# from .models import UserCount
from django.views.generic import View

def mainUrl(request):
    return HttpResponseRedirect('/user')