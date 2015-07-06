__author__ = 'Franklyn'

from pandas import DataFrame
from collections import namedtuple
from Model import Model
import math

class House(Model):

    DWELLING_TYPES = {'single-family', 'townhouse', 'apartment', 'patio', 'loft'}

    POOL_TYPES = {'private', 'community', 'none'}

    DWELLING_COEFFICIENT = 100

    Listing = namedtuple('Listing',
                    ['num_bedrooms', 'num_bathrooms', 'living_area', 'lat', 'lon',
                     'exterior_stories', 'pool', 'dwelling_type',
                     'list_date', 'list_price', 'close_date', 'close_price'])

    Objects = DataFrame(columns=Listing._fields)

    def __default_similarity_callback(self, house1, house2):
        similarity = house1.distance(house2)
        similarity -= House.DWELLING_COEFFICIENT*int(house1.dwelling_type == house2.dwelling_type)
        return similarity

    def __init__(self, listing):
        Model.__init__(self, listing, House.Listing._fields)

    def get_similar(self, n, similarity_callback=None):
        if similarity_callback is None:
            similarity_callback = self.__default_similarity_callback
        return House.Objects.ix[House.Objects.apply(lambda x:similarity_callback(self, x), axis=1).argsort()[:n]]

    def distance(self, to):
        lat1 = self['lat']
        lon1 = self['lon']
        lat2 = to['lat']
        lon2 = to['lon']

        earth_radius = 6371
        x = (lon2 - lon1) * math.cos(0.5 * (lat2 + lat1))
        y = (lat2 - lat1)
        distance_km = earth_radius * math.sqrt(x*x + y*y)

        return distance_km
