from common.base_dao.base import DAO
from common.star.dimension import Dimension
from common.star.fact import Fact
from common.utils.logger import logger
from common.utils.reader import configuration
from common.utils.utils import get_model_class, instanceOf

class Pipeline:
    def __init__(self):
        self.metadata = configuration().get('pipeline')
    def run(self):
        #self.createDimensions()
        self.createFact()
        #self.createMiddleEntities()
        
    def createDimensions(self):
        """ Build all dimensional tables given pipeline information in configuration file """        
        datasource = DAO.from_csv(self.metadata.get('datasource'))
        dimension_tables = self.metadata.get('dimension_tables')
        tuple(map(lambda table: Dimension.build(datasource, self.metadata.get(table)).save(), dimension_tables))
    
    def createFact(self):
        datasource = DAO.from_csv(self.metadata.get('datasource'))
        table_name = self.metadata.get('fact')
        Fact.build(datasource, self.metadata.get(table_name)).save()

    def createMiddleEntities(self):
        """TODO"""
               

        

        
        

