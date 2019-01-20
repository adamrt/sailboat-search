import re

from django.db import models
from autoslug import AutoSlugField

from .scrapers import YachtWorldSearcher


class Boat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name')

    length = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    favorite = models.BooleanField(default=False)

    bluewater = models.BooleanField(default=False)
    bw_url = models.URLField(blank=True)
    sd_url = models.URLField(blank=True)

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @property
    def display_length(self):
        return str(round(self.length, 1) if self.length % 1 else int(self.length))

    @property
    def length_from_name(self):
        # space, group:length(2digits, maybe H- (H-28), maybe decimal and number, maybe letter D (CD 25D, maybe space or EOL
        match = re.search("\s+(H-)?(?P<length>\d{2}(\.\d{1})?)[D]?(\s+|$)", self.name)
        return match.group("length") if match else None

    def import_listings(self):
        searcher = YachtWorldSearcher(self)
        searcher.process()
