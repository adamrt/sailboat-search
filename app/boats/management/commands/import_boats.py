import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from boats.models import Boat

class Command(BaseCommand):
    help = 'Import all boats from bluewater'

    def handle(self, *args, **options):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        url = "http://bluewaterboats.org/about/index/"
        rq = requests.get(url, headers=headers)
        soup = BeautifulSoup(rq.content, 'html.parser')
        boats = soup.select('div.boatimage')
        for boat in boats:
            name = boat.select('a')[0]['title']
            Boat.objects.get_or_create(name=name)

        url = "http://atomvoyages.com/planning/good-old-boats-list.html"
        rq = requests.get(url, headers=headers)
        soup = BeautifulSoup(rq.content, 'html.parser')
        boats = soup.select('div.items-leading table ul li')
        for boat in boats:
            name = boat.select('a')[0].get_text()
            Boat.objects.get_or_create(name=name)

        for boat in Boat.objects.all():
            boat.length = boat.length_from_name
            boat.save()
