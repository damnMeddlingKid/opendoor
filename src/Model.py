__author__ = 'Franklyn'

from pandas import Series, DataFrame
import pandas as pd

class Model(Series):
    """Base Class of Models, Used to represent the structure of data and define behaviours.

    This base class handles tasks that are common to all models such as serialization and saving objects in a collection

    Attributes:
        Objects: Store of model objects created from their respective class.
    """
    @classmethod
    def read_serialized_object(cls, path):
        try:
            cls.Objects = pd.read_pickle(path)
        except Exception as e:
            print "Could not read serialized objects: {0}".format(e.message)
        return cls

    @classmethod
    def write_serialized_object(cls, path):
        try:
            cls.Objects.to_pickle(path)
        except Exception as e:
            print "Could not write serialized objects: {0}".format(e.message)

    @classmethod
    def sort_by(cls, sort_callback, limit=10):
        """Sorts the collection using the callback function and return limit number of elements"""
        return cls.Objects.ix[cls.Objects.apply(lambda x: sort_callback(x), axis=1).argsort()[:limit]]

    def save(self):
        if self.__class__.Objects is None:
            self.__class__.Objects = DataFrame(columns = self.index)
        self.__class__.Objects = self.__class__.Objects.append(self, ignore_index=True)

    def __init__(self, data, fields):
        Series.__init__(self, data, index=fields)

