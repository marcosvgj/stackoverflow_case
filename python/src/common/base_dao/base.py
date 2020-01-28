import abc
from common.utils import spark

NOT_IMPL_MSG = "This method need to be implemented, please check the documentation"

class DAO:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def select(self, db_table):
        raise NotImplementedError(NOT_IMPL_MSG)
        
    @abc.abstractmethod
    def insert(self, db_table, dataframe):
        raise NotImplementedError(NOT_IMPL_MSG)
        
    @staticmethod
    def from_csv(path, header=True):
        return spark.getOrCreate().read.format("csv")\
        .option("header", header).load(path)