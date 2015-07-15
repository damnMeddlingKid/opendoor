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

    # Weighting coefficient for the dwelling type similarity
    DWELLING_COEFFICIENT = 100

    listing = namedtuple('Listing',
                    ['num_bedrooms', 'num_bathrooms', 'living_area', 'lat', 'lon',
                     'exterior_stories', 'pool', 'dwelling_type',
                     'list_date', 'list_price', 'close_date', 'close_price'])

    def __default_similarity_callback(self, house_to):
        """Default similarity metric used by the class if no similarity callback is provided.
        Computes similarity between house1 and house2, similarity is based on the distance between them and a weighted
        cost of the similarity of dwelling type.
        :param house_to:  Series object of second house to compare to
        :return: similarity error between the two houses, lower numbers are more similar
        """
        similarity = self.distance(house_to)
        similarity -= House.DWELLING_COEFFICIENT*int(self.dwelling_type == house_to.dwelling_type)
        return similarity

    def __init__(self, listing):
        super(House,self).__init__(self, listing, House.listing._fields)

    def get_similar(self, num_listings, similarity_callback=None):
        """Returns the n most smilar houses to this house.
        :param num_listings:   Number of houses to return
        :param similarity_callback: A function that compares the similarity between two houses, must take in two parameters
        and return a number where smaller values are more similar.
        :return:    DataFrame of similar houses.
        """
        if similarity_callback is None:
            similarity_callback = self.__default_similarity_callback
        return House.sort_by(similarity_callback, num_listings)

    def distance(self, to_house):
        """Computes the distance from this house to another house using the equirectangular approximation.
        reference: http://www.movable-type.co.uk/scripts/latlong.html
        :param to_house: The house to computer distance to
        :return: distance in kilometers
        """
        lat1 = self['lat']
        lon1 = self['lon']
        lat2 = to_house['lat']
        lon2 = to_house['lon']

        earth_radius = 6371
        x_coordinate = (lon2 - lon1) * math.cos(0.5 * (lat2 + lat1))
        y_coordinate = (lat2 - lat1)
        distance_km = earth_radius * math.sqrt(x_coordinate*x_coordinate + y_coordinate*y_coordinate)

        return distance_km
