import abc

class DAO:
    __metaclass__ = abc.ABCMeta
            
    @staticmethod
    @abc.abstractmethod
    def select(self, db_table):
        NOT_IMPL_MSG = "This method need to be implemented, please check the documentation"
        raise NotImplementedError(NOT_IMPL_MSG)
        
    @staticmethod
    @abc.abstractmethod
    def insert( db_table, data):
        NOT_IMPL_MSG = "This method need to be implemented, please check the documentation"
        raise NotImplementedError(NOT_IMPL_MSG)
        
    @staticmethod
    def from_csv(path, header=True):
        global spark
        return spark.read.format("csv")\
        .option("header", header).load(path)

    @staticmethod
    def instanceOf(subclass):
        try:
            return next(filter(lambda x: x.__name__ == subclass, DAO.__subclasses__()))
        except StopIteration as err:
            raise Exception("Please verify if this feature is implemented already")