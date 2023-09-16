from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(LeadUser)
class LeadUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'age',
                    'location', 'interest', 'phone', 'active']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'created_at', 'times_taken']
    prepopulated_fields = {"slug": ('title',)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display =['id','label','order','quiz']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'is_correct','question']


@admin.register(CorrectAnswer)
class CorrectAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'user', 'correctly_answer']
