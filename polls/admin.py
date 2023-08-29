from .models import Question, Choice, Category
from django.contrib import admin
from .forms import CategoryForm

# Register your models here.


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    inlines = [ChoiceInLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['id', 'category_name']
