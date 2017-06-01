from difflib import SequenceMatcher

from django.core.management.base import BaseCommand, CommandError

from boats.models import Boat
from boats.scrapers import BoatScraper
from listings.models import Listing
from listings.scrapers import ListingScraper

class Command(BaseCommand):
    help = 'Import all boats from bluewater'

    def handle(self, *args, **options):
        for boat in Boat.objects.all()[5:10]:
            ms = BoatScraper(name=boat.name)
            boat.length = ms.length
            boat.save()
            for ms in ms.get_listings():
                ls = ListingScraper(ms)
                print(ls.name)
                if Listing.objects.filter(url=ls.url).exists():
                    continue
                if not ls.name:
                    print('skipping....')
                    continue
                review = SequenceMatcher(None, boat.name.strip().lower(), ls.name.lstrip('01234567890 ').lower()).ratio() < 0.7
                Listing.objects.create(boat=boat, price=ls.price, name=ls.name, year=ls.year, url=ls.url, review=review)
