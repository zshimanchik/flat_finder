from collections import namedtuple

Apartment = namedtuple('Apartment', ['id', 'photo', 'url', 'created', 'price'])


def apartment_to_str(self):
    return "id: {}\n" \
           "photo: {}\n" \
           "url: {}\n" \
           "{}\n" \
           "price: {}".format(self.id, self.photo, self.url, self.created, self.price)
Apartment.__str__ = apartment_to_str