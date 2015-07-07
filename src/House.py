__author__ = 'Franklyn'

from pandas import DataFrame
from collections import namedtuple
from Model import Model
import math

class House(Model):
    """House model defines the attributes and behaviours of a House
    """
    DWELLING_TYPES = {'single-family', 'townhouse', 'apartment', 'patio', 'loft'}

    POOL_TYPES = {'private', 'community', 'none'}

    """Weighting coefficient for the dwelling type similarity"""
    DWELLING_COEFFICIENT = 100

    Listing = namedtuple('Listing',
                    ['num_bedrooms', 'num_bathrooms', 'living_area', 'lat', 'lon',
                     'exterior_stories', 'pool', 'dwelling_type',
                     'list_date', 'list_price', 'close_date', 'close_price'])

    Objects = DataFrame(columns=Listing._fields)

    def __default_similarity_callback(self, house1, house2):
        """Default similarity metric used by the class if no similarity callback is provided.
        Computes similarity between house1 and house2, similarity is based on the distance between them and a weighted
        cost of the similarity of dwelling type.
        :param house1:  Series object of first house
        :param house2:  Series object of second house
        :return: similarity error between the two houses, lower numbers are more similar
        """
        similarity = house1.distance(house2)
        similarity -= House.DWELLING_COEFFICIENT*int(house1.dwelling_type == house2.dwelling_type)
        return similarity

    def __init__(self, listing):
        Model.__init__(self, listing, House.Listing._fields)

    def get_similar(self, n, similarity_callback=None):
        """Returns the n most smilar houses to this house.
        :param n:   Number houses to return
        :param similarity_callback: A function that compares the similarity between two houses, must take in two parameters
        and return a number where smaller values are more similar.
        :return:    DataFrame of similar houses.
        """
        if similarity_callback is None:
            similarity_callback = self.__default_similarity_callback
        return House.Objects.ix[House.Objects.apply(lambda x:similarity_callback(self, x), axis=1).argsort()[:n]]

    def distance(self, to):
        """Computes the distance from this house to another house using the equirectangular approximation.
        reference: http://www.movable-type.co.uk/scripts/latlong.html
        :param to: The house to computer distance to
        :return: distance in kilometers
        """
        lat1 = self['lat']
        lon1 = self['lon']
        lat2 = to['lat']
        lon2 = to['lon']

        earth_radius = 6371
        x = (lon2 - lon1) * math.cos(0.5 * (lat2 + lat1))
        y = (lat2 - lat1)
        distance_km = earth_radius * math.sqrt(x*x + y*y)

        return distance_km
