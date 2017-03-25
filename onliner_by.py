import requests
import json
import time
from dateutil import parser
import datetime
from models import Apartment

def file_cached(func):
    import os
    def wrapper(self, page=1):
        if os.path.exists("data{}.json".format(page)):
            return json.load(open("data{}.json".format(page)))
        else:
            return func(self, page)
    return wrapper


class OnlinerCrawler:
    def __init__(self, since, timezone=None, fetch_delay=1):
        """
        :param since: datetime parameter with timezone for example:
        >>> import datetime
        >>> tz = datetime.timezone(datetime.timedelta(hours=3))
        >>> since = datetime.datetime.now(tz=tz) - datetime.timedelta(days=3)
        """
        self.tz = timezone if timezone is not None else datetime.timezone.utc
        self.now = datetime.datetime.now(tz=self.tz)
        self.fetch_delay = fetch_delay
        self._since = since

    def find(self):
        data = self.get()
        for apartment in self.handle(data, self._since):
            yield apartment

        last_page = self._get_last_page(data)
        for page in range(2, last_page):
            time.sleep(self.fetch_delay)
            data = self.get(page)
            for apartment in self.handle(data, self._since):
                yield apartment

    # @file_cached
    def get(self, page=1):
        url = "https://ak.api.onliner.by/search/apartments?" \
              "only_owner=true" \
              "&price[min]=50" \
              "&price[max]=320" \
              "&currency=usd" \
              "&rent_type[]=1_room" \
              "&rent_type[]=2_rooms" \
              "&rent_type[]=3_rooms" \
              "&rent_type[]=4_rooms" \
              "&bounds[lb][lat]=53.92324551418698" \
              "&bounds[lb][long]=27.635679244995117" \
              "&bounds[rt][lat]=53.94684241751605" \
              "&bounds[rt][long]=27.69576072692871" \
              "&page={page}".format(page=page)

        resp = requests.get(url)
        resp.raise_for_status()
        data = json.loads(resp.text)
        return data

    def _get_last_page(self, data):
        if 'page' in data and 'last' in data['page']:
            return data['page']['last']
        else:
            return 1

    def handle(self, data, since):
        if not 'apartments' in data:
            return

        for apartment in data['apartments']:
            for res in self.handle_apartment(apartment, since):
                yield res

    def handle_apartment(self, apartment, since):
        id = apartment['id']
        url = apartment['url']
        photo = apartment['photo']
        created_at = parser.parse(apartment['created_at'])
        price = apartment['price']['amount']
        if created_at > since:
            created = self._age_to_str(self.now - created_at)
            yield Apartment(id, photo, url, created, price)

    def _age_to_str(self, age):
        if age.days == 0:
            return "created today"
        elif age.days == 1:
            return "created yesterday"
        else:
            return "created {} days ago".format(age.days)


if __name__ == "__main__":
    tz = datetime.timezone(datetime.timedelta(hours=3))
    since = datetime.datetime.now(tz=tz) - datetime.timedelta(hours=14)

    cr = OnlinerCrawler(since, timezone=tz)
    cr.find()