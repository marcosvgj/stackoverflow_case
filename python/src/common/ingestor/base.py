import abc
from common.dao.base import DAO
from common.utils.logger import logger

NOT_IMPL_MSG = 'This method need to be implemented, please check the documentation'

class Ingestor:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError(NOT_IMPL_MSG)
    
    def load(self, metadata, data):
        try:
            sink = metadata.get('sink')
            db_table = f'{metadata.get("database")}.{metadata.get("table")}'
            access = DAO.instanceOf(sink)
            access.insert(db_table=db_table, data=data)
        except Exception as error: 
            logger.error(error)
            
    @staticmethod
    def apply(f, metadata):
        return f(metadata)