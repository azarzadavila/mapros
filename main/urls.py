from django.urls import path

from main import views

urlpatterns = [
    path("ask_state/", views.AskState.as_view()),
]
