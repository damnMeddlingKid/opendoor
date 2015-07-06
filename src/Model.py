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
        cls.Objects = pd.read_pickle(path)
        return cls

    @classmethod
    def write_serialized_object(cls, path):
        cls.Objects.to_pickle(path)

    def save(self):
        self.__class__.Objects = self.__class__.Objects.append(self, ignore_index=True)

    def __init__(self, data, fields):
        Series.__init__(self, data, index=fields)
