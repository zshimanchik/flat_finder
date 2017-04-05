import json
import os
import time
import urllib.parse as urlparse
import logging

import lxml.html
import requests
from requests.exceptions import HTTPError

import models

LOGGER = logging.getLogger(__name__)


class Neagent:
    url = 'http://neagent.by/board/minsk/?hasPhotos=1&catid=1&district=29&subdistrict=5,28&priceMax=350&currency=2'
    PAGE_SIZE = 13
    EXCEPTIONS_FILE = 'exceptions.json'
    exceptions = []
    FETCH_DELAY = 1

    def load_exceptions(self):
        if os.path.exists(self.EXCEPTIONS_FILE):
            with open(self.EXCEPTIONS_FILE, 'r') as f:
                self.exceptions = json.load(f)

    def save_exceptions(self):
        with open(self.EXCEPTIONS_FILE, 'w') as f:
            json.dump(self.exceptions, f, indent=2)

    def find(self):
        self.load_exceptions()
        page_num = 0
        LOGGER.info("parsing: {}".format(page_num))
        try:
            while True:
                for apartment in self.parse_page(page_num):
                    yield apartment
                page_num += 1
                time.sleep(self.FETCH_DELAY)
                LOGGER.info("parsing: {}".format(page_num))
        except HTTPError as ex:
            LOGGER.info("end")
            raise StopIteration()
        finally:
            self.save_exceptions()

    def parse_page(self, page_num):
        resp = requests.get(self.get_url(page_num * self.PAGE_SIZE))
        resp.raise_for_status()
        page = lxml.html.fromstring(resp.text)

        ads = page.xpath("//div[contains(@class, 'sect_body')]/div[contains(@class, 'imd') and not(contains(@class, 'typevip'))]")
        if not ads:
            raise StopIteration()

        for ad in ads:
            appartment = self.try_to_parse_ad(ad)
            if appartment:
                yield appartment

    def get_url(self, skip=0):
        parsed = urlparse.urlparse(self.url)
        return urlparse.urlunsplit((parsed.scheme, parsed.netloc, "{}{}".format(parsed.path, skip), parsed.query, parsed.fragment))

    def try_to_parse_ad(self, ad):
        try:
            return self.parse_ad(ad)
        except Exception:
            pass

    def parse_ad(self, ad):
        href = ad.xpath("./div[contains(@class, 'imd_photo')]/a/@href")[0]
        img = ad.xpath("./div[contains(@class, 'imd_photo')]//img/@src")[0]
        if href not in self.exceptions:
            self.exceptions.append(href)
            return models.Apartment(id=None, photo=img, url=href, created=None, price=None)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for ap in Neagent().find():
        print(ap)
