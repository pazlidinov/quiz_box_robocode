import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from .models import LeadUser, Quiz, Question, Answer, CorrectAnswer
from .forms import LeadUserForm
from .utils import control_send
# Create your views here.


class HomePageView(ListView):
    model = Quiz
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["correct_answwers"] = CorrectAnswer.objects.all(
        ).select_related('author', 'quiz')
        return context


class AddLeadUser(CreateView):
    model = LeadUser
    template_name = 'access_phonenumber.html'
    form_class = LeadUserForm
    success_url = '/access_phonenumber/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.request.session['lead_user_phonenumber'] = self.request.POST.get(
            'phone')
        self.request.session['answer'] = 0
        print(self.request.session['answer'])
        messages.success(self.request, "The task was created successfully.")
        return super(AddLeadUser, self).form_valid(form)


class AccessPhonenumber(TemplateView):
    template_name = 'access_phonenumber.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["phone"] = self.request.session['lead_user_phonenumber']
        user = LeadUser.objects.get(
            phone=self.request.session['lead_user_phonenumber'])
        if not user.password:
            context["answer"] = control_send(user)
        else:
            context["answer"] = True
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = LeadUser.objects.get(
            phone=self.request.session['lead_user_phonenumber'])
        if str(user.password) == request.POST.get('access_code'):
            return redirect('/start_question/special-questions/0/')
        else:
            return redirect('/access_phonenumber/')


def repeat_send(request):
    user = LeadUser.objects.get(
        phone=request.session['lead_user_phonenumber'])
    user.change_password(0)
    return redirect('/access_phonenumber/')


def change_phonenumber(request):
    user = LeadUser.objects.get(
        phone=request.session['lead_user_phonenumber'])
    if request.GET.get('new_phonenumber'):
        user.change_phone(request.GET.get('new_phonenumber'))
        user.change_password(0)
        request.session['lead_user_phonenumber'] = request.GET.get(
            'new_phonenumber')
        request.session.save()
    return redirect('/access_phonenumber/')


class StartQuestion(View):

    def get(self, request, slug, order, *args, **kwargs):
        if request.GET.get('answer'):
            send_answer = Answer.objects.get(id=request.GET.get('answer'))
            if send_answer.is_correct:
                self.request.session['answer'] = self.request.session['answer'] + 1
                self.request.session.save()

        quiz = Quiz.objects.get(slug=slug)
        if order == quiz.question_count:
            return redirect('/result/')
        question = Question.objects.filter(order=order+1, quiz=quiz).first()
        answers = Answer.objects.filter(question=question)
        data = {
            'quiz': quiz,
            'question': question,
            'answers': answers,
            'progress': round((question.order/quiz.question_count)*100),
        }
        return render(request, 'quiz.html', context=data)


class Result(TemplateView):
    template_name = 'quiz _result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(slug='special-questions')
        user = LeadUser.objects.get(
            phone=self.request.session['lead_user_phonenumber'])
        correctly = CorrectAnswer.objects.create(
            author=user, quiz=quiz, correctly_answer=self.request.session['answer'])
        result = round((correctly.correctly_answer/quiz.question_count)*100)
        context["result"] = result
        return context


def check_phone_number(request):
    data = json.loads(request.GET.get("data"))
    if data:
        lead_user = LeadUser.objects.filter(
            phone=int(data.get("phone_number")))
        if lead_user:
            return JsonResponse({"status": 404})
        else:
            return JsonResponse({"status": 200})
    return HttpResponse({"status": 200})


def user_actived(request):
    user = LeadUser.objects.get(phone=request.session['lead_user_phonenumber'])
    user_active = True
    print('ok')
    return HttpResponse({"status": 200})
