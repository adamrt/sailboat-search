from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from autoslug import AutoSlugField

from listings.models import Listing
from listings.scrapers import ListingScraper
from .scrapers import BoatScraper


class Boat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name')

    length = models.PositiveSmallIntegerField(blank=True, null=True)
    bw_url = models.URLField(blank=True)

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @property
    def length_from_name(self):
        nums = self.name.split(" ")[-1]
        if len(nums) == 2 and nums.isdigit():
            nums = int(nums)
            return nums
        else:
            return None

    def refresh_listings(self):
        ms = BoatScraper(name=self.name)
        for ms in ms.get_listings():
            ls = ListingScraper(ms)
            if Listing.objects.filter(url=ls.url).exists():
                continue

            if ls.status_code != 200:
                print('skipping {}... bad page: {}'.format(self.name, ls.url))
                continue

            if ls.name is None:
                print('skipping {}... no name', format(self.name))
                continue

            if self.name.replace("-", " ").split(" ")[0].lower() not in ls.name.lower():
                print('skipping {}.... {} not in {}'.format(self.name, self.name.split(" ")[0], ls.name))
                continue

            if ls.length not in [self.length, self.length + 1, self.length - 1]:
                print('skipping {} ... length {} does not match {}'.format(self.name, self.length, ls.length))
                continue

            # print(ls.name)
            listing, created = Listing.objects.get_or_create(url=ls.url, defaults={"boat": self, "name": ls.name})
            listing.price = ls.price
            listing.name = ls.name
            listing.year = ls.year
            listing.location = ls.location
            if self.length != ls.length:
                listing.review = True

            listing.save()
