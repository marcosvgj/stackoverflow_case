from common.base_dao.base import DAO
from common.star.middleEntity import MiddleEntity
from common.star.dimension import Dimension
from common.star.fact import Fact
from common.utils.logger import logger
from common.utils.reader import configuration
from common.utils.utils import get_model_class

class Pipeline:
    def __init__(self):
        self.metadata = configuration().get('pipeline')
    def run(self):
        self.createDimensions()
        self.createFact()
        self.createMiddleEntities()
        
    def createDimensions(self):
        """ Build all dimensional tables given pipeline information in configuration file """
        try:
            datasource = DAO.from_csv(self.metadata.get('datasource'))
            dimension_tables = self.metadata.get('dimension_tables')
            tuple(map(lambda table: Dimension.build(datasource, self.metadata.get(table)).save(), dimension_tables))
            logger.warn("Dimension's builder ran successfully...")
        except Exception as error:
            logger.error(error)

    def createFact(self):
        try:
            datasource = DAO.from_csv(self.metadata.get('datasource'))
            table_name = self.metadata.get('fact_table')
            Fact.build(datasource, self.metadata.get(table_name)).save()
            logger.warn("Fact builder ran successfully...")
        except Exception as error:
            logger.error(error)

    def createMiddleEntities(self):
        try:
            datasource = DAO.from_csv(self.metadata.get('datasource'))
            dimension_tables = self.metadata.get('middle_entity_tables')
            tuple(map(lambda table: MiddleEntity.build(datasource, self.metadata.get(table)).save(), dimension_tables))
            logger.warn("Middle Entities builder ran successfully...")
        except Exception as error:
            logger.error(error)
               

        

        
        

