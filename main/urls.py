from django.urls import path

from main import views

urlpatterns = [
    path("ask_state/", views.AskState.as_view()),
    path("owned_theorem_statements/", views.OwnedTheoremStatementsViewSet.as_view()),
    path(
        "owned_theorem_statement/<int:pk>/",
        views.OwnedTheoremStatementViewSet.as_view(),
    ),
    path(
        "list_users_not_theorem_statement/<int:pk>/",
        views.ListUserNotAssignedStatementViewSet.as_view(),
    ),
    path("send_statement/", views.SendStatement.as_view()),
    path("theorem_proof/<int:pk>/", views.ProofViewSet.as_view()),
]
