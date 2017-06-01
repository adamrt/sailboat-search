import requests
from bs4 import BeautifulSoup


class BoatScraper(object):
    def __init__(self, name):
        self.name = name

    @property
    def url(self):
        param = '+'.join(self.name.split(' ')).lower()
        # 2279=sail 2285=used
        url = "http://www.yachtworld.com/core/listing/cache/searchResults.jsp?ps=1000&N=2279+2285&Ntt=" + param
        return url

    def get_listings(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup.select("div.listing")

    @property
    def length(self):
        tail = self.name.split(" ")[-1]
        return int(tail) if len(tail) == 2 and tail.isdigit() else None
