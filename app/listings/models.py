from django.db import models
from autoslug import AutoSlugField
from model_utils.fields import StatusField
from model_utils import Choices


class Listing(models.Model):
    STATUS = Choices('', 'no', 'review', 'yes')
    status = StatusField()
    status_note = models.TextField(blank=True)

    boat = models.ForeignKey("boats.Boat", on_delete=models.CASCADE)

    title = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='title')

    price = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=2, blank=True)

    url = models.URLField(unique=True)

    review = models.BooleanField(default=False)

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['boat__name']

    @property
    def site_title(self):
        if 'yachtworld.com' in self.url:
            return 'YW'

        if 'sailboatlistings.com' in self.url:
            return 'SL'

        if 'craigslist.com' in self.url:
            return 'CL'

        return '!!'
