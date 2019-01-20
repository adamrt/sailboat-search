import re
import requests
from bs4 import BeautifulSoup

from listings.models import Listing

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


class SailboatListingsSearcher(object):
    # 2279=sail, 2285=used, ps is per-page results
    url_tmpl  = "http://www.sailboatlistings.com/cgi-bin/saildata/db.cgi?db=default&uid=default&&view_records=+Search+by+Keyword+&keyword={}"

    def __init__(self, boat):
        self.boat = boat
        self.name = boat.name

    @property
    def search_query(self):
        return '+'.join(self.name.split(' ')).lower()

    @property
    def search_url(self):
        return self.url_tmpl.format(self.search_query)

    def process(self):
        req = requests.get(self.search_url, headers=HEADERS)
        soup = BeautifulSoup(req.content, 'html.parser')
        for listing in soup.select("div.listing"):
            item = YachtWorldItem(self.boat, listing)
            item.process()


class YachtWorldSearcher(object):
    # 2279=sail, 2285=used, ps is per-page results
    url_tmpl  = "http://www.yachtworld.com/core/listing/cache/searchResults.jsp?ps=1000&N=2279+2285&Ntt={}"

    def __init__(self, boat):
        self.boat = boat
        self.name = boat.name

    @property
    def search_query(self):
        return '+'.join(self.name.split(' ')).lower()

    @property
    def search_url(self):
        return self.url_tmpl.format(self.search_query)

    def process(self):
        req = requests.get(self.search_url, headers=HEADERS)
        soup = BeautifulSoup(req.content, 'html.parser')
        for listing in soup.select("div.listing"):
            item = YachtWorldItem(self.boat, listing)
            item.process()


class YachtWorldItem(object):
    def __init__(self, boat, soup):
        self.boat_short_name = boat.name.replace("-", " ").split(" ")[0].lower()
        self.soup = soup
        self.boat = boat

    def process(self):
        if self.is_pending or self.is_premier:
            return

        if self.boat_short_name not in self.name.lower():
            return

        if self.boat.length_from_name != self.length_from_name:
            print('{} != {} :: {} || {}'.format(self.boat.length_from_name, self.length_from_name, self.boat.name, self.name))
            return

        listing, created = Listing.objects.get_or_create(url=self.url, defaults={"boat": self.boat, "title": self.name})
        listing.price = self.price
        listing.title = self.name
        listing.year = self.year
        listing.location = self.short_location
        listing.country = self.country or ""
        listing.save()

    @property
    def is_pending(self):
        return bool(self.soup.find('span', {'class': 'active_field'}) )

    @property
    def is_premier(self):
        return 'premier' in self.soup.get('class')

    @property
    def name(self):
        return " ".join(self.soup.find('div', {'class': 'make-model'}).find('a').text.split())

    @property
    def price(self):
        s = self.soup.select('.price')[0].text.strip().replace("US$", "").replace("*", "").replace(",", "").strip()
        return s if not s.startswith('Call') else None

    @property
    def country(self):
        loc = self.location.lower()
        if ', us' in loc:
            return 'US'
        if 'united states' in loc:
            return 'US'

        if 'united kingdom' in loc:
            return 'UK'

        if ', mex' in loc:
            return 'MX'

        if 'mexico' in loc:
            return 'MX'

        if 'france' in loc:
            return 'FR'

    @property
    def short_location(self):
        s = self.location
        s = s.replace('United States', 'USA')
        s = s.replace('United Kingdom', 'GBR')
        s = s.replace('Mexico', 'MEX')
        s = s.replace('Canada', 'CAN')
        return s

    @property
    def location(self):
        return " ".join(self.soup.select('.location')[0].string.split())

    @property
    def length(self):
        return re.search("(?P<length>\d{2}) (ft).?", self.name).group('length')

    @property
    def length_from_name(self):
        # space, group:length(2digits, maybe H- (H-28), maybe decimal and number, maybe letter D (CD 25D, maybe space or EOL
        match = re.search("\s+(H-)?(?P<length>\d{2}(\.\d{1})?)[D]?(\s+|$)", self.name)
        return match.group("length") if match else self.length

    @property
    def year(self):
        s = self.name.split(' ft ')[1]
        year = s[0:4]
        if re.findall(r"[0-9]{4}", year):
            return int(year)
        else:
            return None

    @property
    def url(self):
        base_url = "http://www.yachtworld.com"
        href = self.soup.select("div.make-model a")[0]['href']
        return base_url + href
