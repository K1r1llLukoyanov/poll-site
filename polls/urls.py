from django.urls import path


from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.detail_view, name="details"),
    path("results/<int:pk>", views.Result.as_view(), name="results"),
    path("<int:question_id>/vote", views.vote, name="vote"),
    path("new_poll/", views.new_poll, name="new_poll"),
    path("delete_poll/<int:pk>", views.delete_poll, name="delete_poll"),
    path("edit_poll/<int:pk>", views.edit_poll, name="edit_poll"),
    path("categories/", views.Categories.as_view(), name="categories"),
    path("category/<str:cat>", views.category, name="category"),
    path("category_list/", views.category_list, name="category_list"),
    path("about/", views.about, name="about")
]
