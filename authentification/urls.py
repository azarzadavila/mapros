from django.urls import path

from authentification import views

urlpatterns = [
    path("auth/", views.SignIn.as_view()),
]
