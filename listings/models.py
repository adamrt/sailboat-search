from django.db import models
from autoslug import AutoSlugField



class Listing(models.Model):
    boat = models.ForeignKey("boats.Boat", on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from='name')

    price = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(null=True)
    location = models.CharField(max_length=255)

    url = models.URLField(unique=True)

    review = models.BooleanField(default=False)

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    def __str__(self):
        return self.name
