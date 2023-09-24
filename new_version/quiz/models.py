from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
# Create your models here.

INTEREST = (
    ("frontend", "Web dasturlash Front-End"),
    ("backend", "Web dasturlash Back-End"),
    ("mobil dasturlash", "Mobil dasturlash"),
    ("robototexnika", "Robototexnika"),
    ("grafik dizayn", "Grafik Dizayn"),
    ("3d", "3D modellashtirish"),
)


class LeadUser(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255, blank=True)
    interest = models.CharField(choices=INTEREST, max_length=255, blank=True)
    phone = models.CharField(max_length=255, unique=True)
    password = models.PositiveIntegerField(default=0, blank=True, null=True)
    date_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    send_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    active = models.BooleanField(default=False, null=True, blank=True)

    @property
    def send_plus(self):
        self.send_count += 1
        self.save()

    def change_phone(self, phone):
        self.phone = phone
        self.save()

    def change_password(self, password):
        self.password = password
        self.save()

    def new_date_time(self, new_date_time):
        self.date_time = new_date_time
        self.save()
        
    def user_active(self):
        self.active = True
        self.save()

    def __str__(self):
        return str(self.full_name)


class Quiz(models.Model):
    title = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    times_taken = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='quiz_image/', blank=True, null=True)

    @property
    def question_count(self):
        ''' Method to get num of Qs for this quiz, used in Serializer'''        
        return self.questions.count()

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    label = models.CharField(max_length=150)
    order = models.PositiveIntegerField(blank=True, null=True)
    point = models.FloatField(default=3.3)
    image = models.ImageField(
        upload_to='question_image/', blank=True, null=True)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.quiz)+str(self.order)


class Answer(models.Model):
    text = models.CharField(max_length=150)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return str(self.text)+str(self.question)


class CorrectAnswer(models.Model):
    author = models.ForeignKey(
        LeadUser, on_delete=models.CASCADE, related_name='lead_answers', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_answers', blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,
                             related_name='correct_quiz', blank=True, null=True)
    correctly_answer = models.PositiveIntegerField(
        default=0, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def high_result(self, last_result):
        if self.correctly_answer<last_result:
            self.correctly_answer = last_result
            self.save()

    def __str__(self):
        return str(self.author)
