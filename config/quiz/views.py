import json
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import  messages
from django.views.generic import ListView
from django.http import HttpResponse
from .models import LeadUser, Quiz, Question, Answer, CorrectAnswer
from .forms import LeadUserForm
from .utils import make_access_password
# Create your views here.


class HomePageView(ListView):
    model = Quiz
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["correct_answwers"] = CorrectAnswer.objects.all()
        return context

def addLeadUser(request):
    if request.method == "POST":
        form =  LeadUserForm(request.POST)
        if form.is_valid():            
                   
            if make_access_password(request): 
                form.save()         
                request.session['lead_user_phone'] = request.POST.get('phone')
                messages.add_message(request, messages.SUCCESS, 'ROYXATDAN OTILDI')                             
                context={
                'phone_number':request.POST.get('phone'),
                'sms':True,
                }
            else:
                lead=LeadUser.objects.get(phone=request.POST.get('phone'))
                lead.delete()
                context={
                'phone_number':request.POST.get('phone'),
                'sms':False,
                }                
            return render(request, 'access_phonenumber.html', context=context)
        else:
            messages.add_message(request, messages.ERROR, 'FORMA XATO TOLDIRILDI')          
            return redirect('/')
        
def change_phonenumber(request,phonenumber):
    lead=LeadUser.objects.get(phone=phonenumber)
    lead.delete()
    return redirect('/')

def repeat_access_password(request):
    if make_access_password(request):                         
        context={
        'phone_number':request.POST.get('phone'),
        'sms':True,
        }
    else:        
        context={
        'phone_number':request.POST.get('phone'),
        'sms':False,
        }
    return render(request, 'access_phonenumber.html', context=context)  

def access_phonenumber(request):    
    password_base = request.session['lead_user_password']
    context={
        'phone_number':request.session['lead_user_phone'],
        'sms':True,
    }
    if password_base ==request.POST.get('access_code'):
        return redirect('/question')    
    return render(request, 'access_phonenumber.html',context=context)


def question(request):
    quiz=Quiz.objects.get(title='Special Questions')
    try: 
        lead=LeadUser.objects.get(phone=request.session['lead_user_phone'])
        CorrectAnswer.objects.create(author=lead, quiz=quiz)  
    except:
        return redirect('/')
    
    all_questions =quiz.questions.all()
    first_question =all_questions.first()
    question_count = all_questions.count()
    answers=Answer.objects.filter(question=first_question)
    proggress=round((first_question.order/question_count)*100)
      
    context={
        'title':quiz.title,
        'question':first_question,
        'question_count':question_count,
        'answers':answers,
        'proggress':proggress,
        'clock':question_count*60,
        
        }    
    return render(request, 'quiz.html', context)

def next_question(request):
    quiz=Quiz.objects.get(title='Special Questions')
    lead_user=LeadUser.objects.get(phone=request.session['lead_user_phone'])
    correctAnswer=CorrectAnswer.objects.filter(author=lead_user).first()  
 
    if request.POST.get('answer')!='0' and request.POST.get('answer')!='':
        send_answer_id=int(request.POST.get('answer') )  
        send_answer=Answer.objects.filter(id=send_answer_id).first()    
        if send_answer.is_correct:
            correctAnswer.plus_correct_answer       
    
    all_questions =quiz.questions.all()
    next_question_order=int(request.POST.get('question'))+1    
    next_question=all_questions.get(order=next_question_order)
    answers=Answer.objects.filter(question=next_question)
    question_count = all_questions.count()
    proggress=round((next_question.order/question_count)*100)
    context={
        'title':quiz.title,
        'question':next_question,
        'question_count':question_count,
        'answers':answers,
        'proggress':proggress,
        'clock':request.POST.get('clock')
    }    
    if next_question.order!=question_count:
        return render(request, 'quiz.html', context)
    else:
        result=round((correctAnswer.correctly_answer/question_count)*100)
        data={
            'result':result,
        }
        return render(request, 'quiz _result.html', context=data)
    
def check_phone_number(request):    
    data = json.loads(request.GET.get("data"))       
    if data:        
        lead_user=LeadUser.objects.filter(phone=int(data.get("phone_number")))
        if lead_user:        
            return JsonResponse({"status": 404})
        else:
            return JsonResponse({"status": 200})
    return HttpResponse({"status": 200})