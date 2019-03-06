from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('analysis',views.DashBoarClass.as_view(),name = 'analysis'),
    path('monitor',views.DashBoarClass.as_view(),name = 'monitor'),
]