from django.urls import path

from authentification import views

urlpatterns = [
    path("auth/", views.SignIn.as_view()),
    path("auth/check/", views.TokenCheck.as_view()),
    path("create_account/", views.CreateAccount.as_view()),
    path("confirm_account/<url>/", views.ConfirmAccount.as_view()),
    path("ask_reset/", views.AskReset.as_view()),
    path("check_reset/<url>/", views.CheckReset.as_view()),
    path("reset_password/<url>/", views.ResetPassword.as_view()),
]
