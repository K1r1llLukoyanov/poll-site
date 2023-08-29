from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Question, Choice, Vote, Category
from .serializers import CategorySerializer
from .forms import CreateQuestionForm, CreateChoiceForm
# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


def detail_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.pub_date > timezone.now():
        raise Http404()
    if request.user.is_authenticated:
        if question.created_by == request.user:
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        try:
            Vote.objects.get(voted_by=request.user, question=question)
            return render(request, "polls/results.html", {"question": question})
        except Vote.DoesNotExist:
            pass
    return render(request, "polls/details.html", {"question": question})


class Result(generic.DetailView):
    template_name = "polls/results.html"
    context_object_name = "question"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login:index"))

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html",
                      {
                            "question": question,
                            "error_message": "You didn't select a choice"
                       })
    else:
        Vote.objects.create(question=question, voted_on=selected_choice, voted_by=request.user)
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))


def new_poll(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login:index"))

    if request.method == "POST":
        created_by = request.user
        question_text = request.POST["question_text"]
        pub_date = timezone.now()
        new_question = Question(question_text=question_text, created_by=created_by, pub_date=pub_date, category_id=6)
        new_question.save()

        index = 1
        while True:
            value = request.POST.get(f"choice_text_{index}", None)
            print(value)
            if value:
                new_question.choice_set.create(choice_text=value)
            else:
                break
            index += 1

        return HttpResponseRedirect(reverse("polls:index"))

    elif request.method == "GET":
        q_form = CreateQuestionForm()

        return render(request, "polls/new_poll.html",
                      {
                        "question_form": q_form,
                      })


def delete_poll(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login:index"))

    poll = get_object_or_404(Question, pk=pk)
    if request.method == "GET":
        return render(request, "polls/delete_poll.html", {"question": poll})

    elif request.method == "POST":
        if poll.created_by != request.user:
            return render(request, "polls/delete_poll.html", {
                "error_messages": ["Permission denied"],
                "question": poll
            })
        poll.delete()
    return HttpResponseRedirect(reverse("polls:index"))


def edit_poll(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login:index"))

    poll = get_object_or_404(Question, pk=pk)

    if poll.created_by != request.user:
        return render(request, "polls/results.html", {"error_messages": ["You can edit this poll"], "question": poll})

    if request.method == "GET":
        q_form = CreateQuestionForm()
        q_form.data["question_text"] = poll.question_text
        return render(request, "polls/edit_poll.html", {
            "question_form": q_form,
            "question": poll
        })

    elif request.method == "POST":
        index = 1
        while True:
            value = request.POST.get(f"choice_text_{index}", None)
            if value:
                pass
            else:
                break

        poll.question_text = request.POST["question_text"]
        poll.save()
        return HttpResponseRedirect(reverse("polls:results", args=(poll.id,)))


class Categories(generic.ListView):
    template_name = "polls/all_categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.all().order_by("-pub_date")


def category(request, cat):
    polls = Question.objects.filter(category__category_name=cat, pub_date__lte=timezone.now()).order_by("-pub_date")
    return render(request, "polls/category.html", {"polls": polls, "category": cat})


def about(request):
    return render(request, 'polls/about.html', {})


@csrf_exempt
def category_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)