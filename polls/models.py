from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    category_name = models.CharField("category", max_length=30, unique=True)
    img = models.ImageField(upload_to="polls/images", default=None, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=201)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?"
    )
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= timezone.now() - timezone.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voted_on = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

