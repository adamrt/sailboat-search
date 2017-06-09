import re

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from autoslug import AutoSlugField

from listings.models import Listing
from listings.scrapers import ListingScraper
from .scrapers import BoatScraper


class Boat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name')

    length = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    favorite = models.BooleanField(default=False)

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
        ms = BoatScraper(name=self.name)
        for ms in ms.get_listings():
            ls = ListingScraper(ms)
            if ls.status_code != 200:
                print('skipping {}... bad page: {}'.format(self.name, ls.url))
                continue

            if ls.name is None:
                print('skipping {}... no name', format(self.name))
                continue

            if Listing.objects.filter(url=ls.url).exists():
                continue

            if self.name.replace("-", " ").split(" ")[0].lower() not in ls.name.lower():
                print('skipping {}.... {} not in {}'.format(self.name, self.name.split(" ")[0], ls.name))
                continue


            if self.length_from_name != ls.length_from_name:
                print('skipping {} ... boat length: {} does not match listing length: {}'.format(self.name, self.length_from_name, ls.length_from_name))
                continue

            listing, created = Listing.objects.get_or_create(url=ls.url, defaults={"boat": self, "title": ls.name})
            listing.price = ls.price
            listing.title = ls.name
            listing.year = ls.year
            listing.location = ls.location
            listing.save()
