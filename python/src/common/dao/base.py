import abc
from common.utils import spark

NOT_IMPL_MSG = "This method need to be implemented, please check the documentation"

class DAO:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def select(self, db_table):
        raise NotImplementedError(NOT_IMPL_MSG)
        
    @staticmethod
    @abc.abstractmethod
    def insert( db_table, data):
        raise NotImplementedError(NOT_IMPL_MSG)
        
    @staticmethod
    def from_csv(path, header=True):
        return spark.getOrCreate().read.format("csv")\
        .option("header", header).load(path)

    @staticmethod
    def instanceOf(subclass):
        try:
            return next(filter(lambda x: x.__name__ == subclass, DAO.__subclasses__()))
        except StopIteration as error:
            raise Exception(f'Please verify if this feature is implemented already: {error}')