__author__ = 'Franklyn'

from pandas import Series, DataFrame
import pandas as pd

class Model(Series):

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
