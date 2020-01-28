import abc
from common.base_dao.base import DAO
from common.utils.logger import logger

NOT_IMPL_MSG = 'This method need to be implemented, please check the documentation'

class Ingestor:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def save(self):
        raise NotImplementedError(NOT_IMPL_MSG)
    
    @abc.abstractmethod
    def insert(self):
        raise NotImplementedError(NOT_IMPL_MSG)
            
    @staticmethod
    def apply(f, metadata):
        return f(metadata)