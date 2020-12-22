from django.urls import path

import sets.views as views

urlpatterns = [path("ask/", views.Ask.as_view())]
