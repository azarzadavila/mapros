from django.db import models


class ProofModel(models.Model):
    statement = models.TextField()
    statement_proof = (
        models.TextField()
    )  # TODO maybe a CharField with restricted size is better
    parent = models.ForeignKey("self", blank=True, on_delete=models.CASCADE)
