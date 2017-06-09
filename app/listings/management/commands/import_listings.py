from difflib import SequenceMatcher

from django.core.management.base import BaseCommand, CommandError

from boats.models import Boat
from listings.models import Listing

class Command(BaseCommand):
    help = 'Import all boats from bluewater'

    def handle(self, *args, **options):
        for boat in Boat.objects.all():
            boat.import_listings()
