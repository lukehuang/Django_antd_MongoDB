from django.shortcuts import render,HttpResponse

from django.views.generic import View

class DashBoarClass(View):
    def get(self,request):
        return render(request, 'user/index.html')
