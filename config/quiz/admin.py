from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(LeadUser)
class LeadUserAdmin(admin.ModelAdmin):
    list_display=['id','full_name', 'age', 'location','interest','phone']
    
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display=['id','title', 'created_at', 'times_taken']
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # list_display=['id','label', 'order', 'point']
    pass
    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=['id','text', 'is_correct']
    
@admin.register(CorrectAnswer)
class CorrectAnswerAdmin(admin.ModelAdmin):
    list_display=['id','author', 'correctly_answer']


