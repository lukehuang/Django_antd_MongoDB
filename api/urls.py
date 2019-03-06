from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    # 登录页面
    path('login/account',views.Login.as_view(),name = 'login'),
    path('currentUser/',views.CurrentUserClass.as_view(),name = 'currentUser'),
    path('fake_chart_data/',views.FakeChartDataClass.as_view(),name = 'fakeChartData'),
    path('tags/',views.TagsClass.as_view(),name = 'tag'),
    path('register',views.RegisterClass.as_view(),name = 'register'),

]