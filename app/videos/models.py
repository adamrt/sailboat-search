from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from autoslug import AutoSlugField


class Video(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name')

    length = models.PositiveSmallIntegerField(blank=True, null=True)
    favorite = models.BooleanField(default=False)

    bw_url = models.URLField(blank=True)
    sd_url = models.URLField(blank=True)

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
