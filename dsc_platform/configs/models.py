from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
