from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # authenticated
    path('login/', views.my_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),

    # HOMEPAGE
    path("", views.HomePageView.as_view(), name='home'),

    # for leaduser
    path('add_lead_user/', views.AddLeadUser.as_view(), name='add_lead_user'),
    path('access_phonenumber/', views.AccessPhonenumber.as_view(),
         name='access_phonenumber'),

    path('check_phone_number/', views.check_phone_number,
         name='check_phone_number'),
    path('access_phonenumber/check_phone_number/',
         views.check_phone_number, name='check_phone_number'),

    path('repeat_send/', views.repeat_send, name='repeat_send'),
    path('change_phonenumber/', views.change_phonenumber,
         name='change_phonenumber'),

    # for question
    path('start_question/<slug:slug>/<int:order>/',
         views.StartQuestion.as_view(), name='start_question'),
    path('result/<slug:slug>/', views.Result.as_view(), name='result'),
    path('user_actived/', views.user_actived, name='user_actived'),
]
