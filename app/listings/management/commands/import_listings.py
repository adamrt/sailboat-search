from difflib import SequenceMatcher

from django.core.management.base import BaseCommand, CommandError

from boats.models import Boat
from listings.models import Listing

class Command(BaseCommand):
    help = 'Import all boats from bluewater'
    # def add_arguments(self, parser):
    #     parser.add_argument('boat_name', nargs='+', type=str, default=None)


    def handle(self, *args, **options):
        # if options.get('boat_name'):
        #     boats = Boat.objects.filter(name=options.get('boat_name')[0])
        # else:
        boats = Boat.objects.all()

        for boat in boats:
            boat.import_listings()
