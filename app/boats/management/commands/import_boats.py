import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from boats.models import Boat


class Command(BaseCommand):
    help = "Import boat models from multiple sources"

    ignore_boats = [
        "adams 13 metre",  # meters
        "gemini 105m",  # meters
        "sea sprite 27/28",  # length
        "rhodes ranger 28/29",  # length
        "cape dory 25",  # not bw, 25d is
        "catalina 27",  # needs lots of work and too many of them
        "westerly centaur 26",  # england and old
    ]

    extra_boats = [("Hunter 33.5", False), ("Hunter 35.5", False), ("Niagara 35", True)]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    @property
    def bluewater_boats(self):
        url = "http://bluewaterboats.org/about/index/"
        rq = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(rq.content, "html.parser")
        boats = soup.select("div.boatimage")
        return [(boat.select("a")[0]["title"], True) for boat in boats]

    @property
    def atom_boats(self):
        url = "http://atomvoyages.com/planning/good-old-boats-list.html"
        rq = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(rq.content, "html.parser")
        boats = soup.select("div.items-leading table ul li")
        return [(boat.select("a")[0].get_text(), True) for boat in boats]

    def handle(self, *args, **options):
        names = self.extra_boats + self.bluewater_boats + self.atom_boats
        for name, bw in names:
            print(name)
            if name.lower() in self.ignore_boats:
                continue

            boat, created = Boat.objects.get_or_create(name=name)
            if created:
                print("Adding: {}".format(name))
            else:
                print("Updating: {}".format(name))

            boat.length = boat.length_from_name
            boat.bluewater = bw
            boat.save()
