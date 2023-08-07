from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [    
    path("", views.HomePageView.as_view(), name='home'),
    path('add_lead_user/', views.addLeadUser, name='add_lead_user'),
    path('question/', views.question, name='question'),
    path('nex_question/', views.next_question, name='nex_question'),
    
    
    path('access_phonenumber/', views.access_phonenumber, name='access_phonenumber'),    
    path('change_phonenumber/<int:phonenumber>', views.change_phonenumber, name='change_phonenumber'),
    path('repeat_access_password/', views.repeat_access_password, name='repeat_access_password'),
    path('check_phone_number/', views.check_phone_number, name='check_phone_number'),
]
