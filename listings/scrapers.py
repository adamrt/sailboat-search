import re

import requests
from bs4 import BeautifulSoup


class ListingScraper(object):
    def __init__(self, blob):
        self.blob = blob
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = requests.get(self.url, headers=headers)
        self.status_code = req.status_code

        self.soup = BeautifulSoup(req.content, 'html.parser')

    @property
    def name(self):
        if self.soup.select('.boat-title h1'):
            return self.soup.select('.boat-title h1')[0].string
        else:
            print('bad title')
            print(self.soup.select('.boat-title h1'))
            return None

    @property
    def price(self):
        if self.soup.select('.boat-price'):
            price = self.soup.select('.boat-price')[0].string.replace("US$", "").replace(",", "").strip()
            try:
                return int(price)
            except ValueError:
                pass
        return None

    @property
    def location(self):
        if self.soup.select('.boat-location'):
            return self.soup.select('.boat-location')[0].string
        else:
            return ""

    @property
    def length(self):
        length_field = self.soup.find('div', class_='firstColumn').find('dt', text='Length:')
        length = length_field.find_next_sibling('dd').text.strip("'").strip()
        try:
            return int(length)
        except ValueError:
            return None

    @property
    def year(self):
        year = self.name[0:4]
        if re.findall(r"[0-9]{4}", year):
            return int(year)
        else:
            return None

    @property
    def url(self):
        base_url = "http://www.yachtworld.com"
        href = self.blob.select("div.image-container a")[0]['href']
        return base_url + href
