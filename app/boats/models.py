import re

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from autoslug import AutoSlugField

from listings.models import Listing
from listings.scrapers import ListingScraper
from .scrapers import BoatScraper


class Boat(models.Model):
    # LOVE = 1
    # HATE = -1

    # STATUS_CHOICES = (
    #     (LOVE, 'Love'),
    #     (HATE, 'Hate'),
    # )

    # status = models.SmallIntegerField(choices=STATUS_CHOICES)
    # status_note = models.TextField(blank=True)

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
    def length_from_name(self):
        match = re.search("\s+\d{2}(\s+|$)", self.name)
        if match:
            return match.group().strip()
        else:
            return None

    def import_listings(self):
        ms = BoatScraper(name=self.name)
        for ms in ms.get_listings():
            mark_review = False
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


            # not exact but close
            if ls.length in [self.length + 1, self.length - 1]:
                # make sure length of boat is in listing title
                # hallberg 35 lengths shows 34, same with 31->32
                if ls.length_from_name:
                    mark_review = False
                    if self.length != ls.length_from_name:
                        print('skipping {} ... length {} does not match {}'.format(self.name, self.length, ls.length))
                        continue
                    else:
                        print('length equals lengthfromname')
                else:
                    print('length not ok, but no length from name')

                    mark_review = True
            else:
                print('length ok')

            print(ls.name)
            listing, created = Listing.objects.get_or_create(url=ls.url, defaults={"boat": self, "title": ls.name})
            listing.price = ls.price
            listing.title = ls.name
            listing.year = ls.year
            listing.location = ls.location
            listing.review = mark_review
            listing.save()
