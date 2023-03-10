from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.functions import Coalesce
from model_utils.models import TimeStampedModel


class ArtistManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            approved_albums=Coalesce(models.Count("album"), 0)
        )


class Artist(TimeStampedModel):

    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    social_media_link = models.URLField(max_length=200)
    objects = ArtistManager()

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return "{}, {}".format(self.name, self.social_media_link)
