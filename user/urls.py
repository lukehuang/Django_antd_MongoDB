from django.urls import path
# from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    path('',views.User.as_view(),name='user'),
    path('login/',views.User.as_view(),name='login'),
    path('register/',views.User.as_view(),name='register'),
]