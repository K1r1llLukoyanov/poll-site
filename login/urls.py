from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('logging', views.logging, name="logging"),
    path('reg_new_user', views.reg_new_user, name="reg_new_user"),
    path('logout', views.logout_view, name="logout")
]