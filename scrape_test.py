from bs4 import BeautifulSoup
from scrapeIOCRefac import Weather
#import logging


class TestCardiff:
    weather = Weather("testWeb/Cardiff.html", file_path=True)

    def test_maxCardiff(self):
        assert self.weather.getMaxT() == 12

    def test_minCardiff(self):
        assert self.weather.getMinT() == 8

    def test_locCardiff(self):
        assert self.weather.getLoc() == "Cardiff"

class TestHendred:
    weather = Weather("testWeb/Hendred.html", file_path=True)

    def test_maxHendred(self):
        assert self.weather.getMaxT() == 11

    def test_minHendred(self):
        assert self.weather.getMinT() == 7

    def test_locHendred(self):
        assert self.weather.getLoc() == "Hendred"
