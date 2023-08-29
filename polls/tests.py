import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Category


def create_question(question_text, days, category, user):
    """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
    """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, category=category, created_by=user)


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in future"""
        time = timezone.now() + datetime.timedelta(days=30)
        category = Category.objects.create(category_name='Games')
        future_question = Question(pub_date=time, category=category)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        category = Category.objects.create(category_name='Games')
        old_question = Question(pub_date=time, category=category)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """was_published_recently() returns True for questions whose pub_date is within last day"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        category = Category.objects.create(category_name='Games')
        recent_question = Question(pub_date=time, category=category)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displays
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_past_question(self):
        """
        Questions with pub_date in the past are displayed on the index page
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        question = create_question(question_text="Past question.", days=-30, category=category, user=user)
        print(question.created_by_id)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question(self):
        """
        Questions with pub_date in the future aren't displayed on the index page.
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        create_question(question_text="Future question.", days=30, category=category, user=user)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        question = create_question(question_text="Past question.", days=-30, category=category, user=user)
        create_question(question_text="Future question.", days=30, category=category, user=user)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_two_past_questions(self):
        """
        Displays two past questions
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        question1 = create_question(question_text="Past question 1", days=-30, category=category, user=user)
        question2 = create_question(question_text="Past question 2", days=-5, category=category, user=user)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1]
        )


class QuestionDetailsViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of question with a pub date in the future returns a 404 not found.
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        future_question = create_question(question_text="Future question.", days=5, category=category, user=user)
        url = reverse("polls:details", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of past question with pub date in the past displays the question's text.
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        past_question = create_question(question_text="Past question.", days=-5, category=category, user=user)
        url = reverse("polls:details", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTest(TestCase):
    def test_future_question(self):
        """
            The view of result of poll with pub date in the future returns 404 not found
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        future_question = create_question("Future question.", days=30, category=category, user=user)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
            The view of result of poll with pub date in the past displays the question's text
        """
        category = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        past_question = create_question("Future question.", days=-30, category=category, user=user)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        

class CategoriesListViewTest(TestCase):
    def test_no_categories(self):
        """
            Displays the view for categories list, returns empty array of categories and
            prints "No categories are available"
        """
        response = self.client.get(reverse("polls:categories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No categories are available")
        self.assertQuerySetEqual(
            response.context["categories"],
            []
        )

    def test_one_category(self):
        """
            Displays the list view with one category
        """
        category = Category.objects.create(category_name="Games")
        response = self.client.get(reverse("polls:categories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, category.category_name)
        self.assertQuerySetEqual(
            response.context["categories"],
            [category]
        )

    def test_two_categories(self):
        """
            Displays the list view with two categories
        """
        category1 = Category.objects.create(category_name="Games")
        category2 = Category.objects.create(category_name="Science")
        response = self.client.get(reverse("polls:categories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, category1.category_name)
        self.assertContains(response, category2.category_name)
        self.assertQuerySetEqual(
            response.context["categories"],
            [category1, category2]
        )


class CategoryListViewTest(TestCase):
    def test_no_polls(self):
        """
            Displays the list view of some category, returns no polls
            prints "No polls are available"
        """
        category1 = Category.objects.create(category_name="Games")
        url = reverse("polls:category", args=(category1.category_name, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"No polls in category {category1.category_name} are available")
        self.assertQuerySetEqual(
            response.context["polls"],
            []
        )

    def test_one_poll(self):
        """
            Displays the list view of some category with one poll
        """
        category1 = Category.objects.create(category_name="Games")
        user = User.objects.create(username="Kirill")
        question = create_question(question_text="CS:GO or Valorant?", days=-30, category=category1, user=user)
        url = reverse("polls:category", args=(category1.category_name, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["polls"],
            [question]
        )
