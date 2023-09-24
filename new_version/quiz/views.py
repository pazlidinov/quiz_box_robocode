import json
from random import randint
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
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def my_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            print("OK")
            return redirect('quiz:profile')
        else:
            # No backend authenticated the credentials
            print("error")
            return redirect("/")
    return render(request, "index.html")


def logout(request):
    logout(request)
    return redirect("/")


class Profile(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sort for quiz
        quiz_query = Quiz.objects.all().exclude(slug='special-questions')
        quiz_list = [quiz for quiz in quiz_query]
        question_quiz_count = [item.question_count for item in quiz_query]
        context['quiz_count'] = len(quiz_list)
        context['question_quiz_count'] = sum(question_quiz_count)

        # aort for corectly answers
        special_quiz = Quiz.objects.get(slug='special-questions')
        corectly = CorrectAnswer.objects.filter(
            user=self.request.user).exclude(quiz=special_quiz)
        corectly_list = [corect for corect in corectly]
        corectly_count = len(corectly_list)
        corectly_answer_count = [
            item.correctly_answer for item in corectly_list]
        context["corectly_count"] = corectly_count
        context['corectly_answer_count'] = sum(corectly_answer_count)

        # user's appropriation
        print(sum(question_quiz_count))
        context['mistake'] = sum(question_quiz_count) - \
            sum(corectly_answer_count)
        try:
            context['increase'] = (
                (sum(corectly_answer_count)/sum(question_quiz_count))*100)
        except:
            context['increase'] = 0

        # take the other quizs
        corectly_quiz = [item.quiz for item in corectly_list]
        others_quiz = [
            quiz for quiz in quiz_list if quiz not in corectly_quiz][:4]
        context['others_quiz'] = others_quiz

        return context


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
            return redirect('/start_question/it-da-siz-kimsiz/1/')
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


def answer_in_session(request, order):
    try:
        return request.session['answer']
    except:
        request.session['answer'] = 0
        return request.session['answer']


class StartQuestion(View):

    def get(self, request, slug, order, *args, **kwargs):
        
        if request.GET.get('answer'):

            send_answer = Answer.objects.get(id=request.GET.get('answer'))
            if send_answer.is_correct:
                answer_in_session(self.request, order)
                self.request.session['answer'] = self.request.session['answer'] + 1
                self.request.session.save()

        quiz = Quiz.objects.get(slug=slug)
        if quiz.question_count == 0:
            return redirect('/')
        if order == quiz.question_count:
            return redirect('quiz:result', slug)

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
    template_name = 'overall_ratings.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(slug=slug)
        context['quiz'] = quiz
        try:
            if self.request.user.is_authenticated:
                try:
                    correctly = CorrectAnswer.objects.get(
                        user=self.request.user, quiz=quiz)
                    correctly.high_result(self.request.session['answer'])
                except:
                    correctly = CorrectAnswer.objects.create(
                        user=self.request.user, quiz=quiz, correctly_answer=self.request.session['answer'])
            else:
                lead_user = LeadUser.objects.get(
                    phone=self.request.session['lead_user_phonenumber'])
                correctly = CorrectAnswer.objects.create(
                    author=lead_user, quiz=quiz, correctly_answer=self.request.session['answer'])
            result = round(
                (correctly.correctly_answer/quiz.question_count)*100)
            context["result"] = result
        except:
            result = round(
                (self.request.session['answer']/quiz.question_count)*100)
            context["result"] = result
        finally:
            ratings = [
                 {
                    'rating':randint(10, 30),
                    'text':'Marketing,ijtimoiy tarmoqlardan foydalana olish.',
                    'stack':'SMM mutahassisi'
                    },
                    {
                    'rating':randint(40, 88),
                    'text':'Algoritmlar,muammolarga yechim topish,intizom.',
                    'stack':'Back-End'
                    },
                    {
                    'rating':randint(50, 92),
                    'text':'Kreativlik,ilg\'or go\'yalar,noodatiy yondashuv.',
                    'stack':'Front-End'
                    },
                    {
                    'rating':randint(20, 35),
                    'text':'Injenerlik,ixtirolar qilish,texnik bilimlar.',
                    'stack':'Robototexnika'
                    },
                    {
                    'rating':randint(50, 80),
                    'text':'Ijodkorlik,go\'zallik yaratish, qulaylik.',
                    'stack':'Grafik dizayn'
                    },
                ]
            sorted_rating = [x for x in sorted(ratings,key=lambda i:i.get("rating") ,reverse=True,)]
            context["ratings"] = sorted_rating
            return context


def check_phone_number(request):
    data = json.loads(request.GET.get("data"))

    if data:
        lead_user = LeadUser.objects.filter(
            phone=int(data.get("phone_number")))
        user = lead_user.exclude(active=True).delete()
        print(user)
        if lead_user:
            return JsonResponse({"status": 404})
        else:
            return JsonResponse({"status": 200})
    return HttpResponse({"status": 200})


def user_actived(request):
    user = LeadUser.objects.filter(
        phone=request.session['lead_user_phonenumber'])
    user.user_active()
    del request.session['answer']
    return HttpResponse({"status": 200})


class Ratings(TemplateView):
    template_name = 'overall_ratings.html'
