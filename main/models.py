from django.contrib.auth.models import User
from django.db import models


class TheoremStatement(models.Model):
    name = models.CharField(max_length=150)
    hypotheses = models.TextField()
    goal = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)


class ProofForTheoremUser(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    theorem_statement = models.ForeignKey(to=TheoremStatement, on_delete=models.CASCADE)
    proof = models.TextField(blank=True)

    class Meta:
        unique_together = ["user", "theorem_statement"]
