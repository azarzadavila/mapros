from django.urls import path

from formal import views

urlpatterns = [
    path("check_sentence/", views.CheckSentence.as_view()),
]
