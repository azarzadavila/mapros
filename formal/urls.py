from django.urls import path

from formal import views

urlpatterns = [
    path("check_sentence/", views.CheckXmlSentence.as_view()),
    path("text_to_xml/", views.TextToXmlSentence.as_view()),
    path("check_sentence_proof/", views.CheckSentenceProof.as_view()),
    path("check_standalone/", views.CheckStandAloneProof.as_view()),
]
