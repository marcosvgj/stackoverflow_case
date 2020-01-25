from common.dao.base import DAO
from common.kimball.dimension import Dimension
from common.utils.logger import logger
from common.utils.reader import configuration
from model.models import CommunicationToolModel

class Pipeline:
    def __init__(self):
        self.metadata = configuration().get('pipeline')
    
    def run(self):
        self.createDimensions()
    
    def createDimensions(self):
        """ Build all dimensional tables given pipeline information in configuration file """        
        try:
            datasource = DAO.from_csv(self.metadata.get('datasource'))
            datasource.printSchema()
            dimension_tables = self.metadata.get('dimension_tables')
            tuple(map(lambda x: Dimension.build(datasource, self.metadata.get(x)).save(), dimension_tables))
        except Exception as error: 
            logger.error(error)

    def createFact(self):
        """TODO"""
    

        

        
        

