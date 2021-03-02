from django.urls import path

from leanserver import views

urlpatterns = [
    path("sync/", views.Sync.as_view()),
    path("state/", views.StateAt.as_view()),
    path("start/", views.Start.as_view()),
    path("end/", views.End.as_view()),
]
