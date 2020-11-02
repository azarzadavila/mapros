from django.db import models


class ProofModel(models.Model):
    sentence = models.TextField()
    sentence_proof = (
        models.TextField()
    )  # TODO maybe a CharField with restricted size is better
    parent = models.ForeignKey("self", blank=True, on_delete=models.CASCADE)
    parent_position = models.PositiveIntegerField()

    class Meta:
        unique_together = ["parent", "parent_position"]
