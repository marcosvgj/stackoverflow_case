from pyspark.sql.functions import col, explode, split, when, lit
from pyspark.sql.window import Window
from model.models import *
from dao.postgres import PostgresDAO
from common.utils.logger import logger
from common.ingestor.base import Ingestor
from common.utils.utils import get_model_class
from business.rules import MiddleEntityRules

class MiddleEntity(Ingestor):
    def __init__(self, source, model, field, options, database='default', table='table', sink=PostgresDAO,
                 embbebedList=False):
        self.metadata = dict({
            'source': source,
            'database': database,
            'table': table,
            'sink': sink,
            'model': model,
            'embbebedList': embbebedList,
            'description_field': field,
            'options': options
        })

    def get(self):
        return Ingestor.apply(MiddleEntityRules.generate_intermediary_entity, self.metadata)
            
    def save(self):
        data = self.get()
        self.insert(self.metadata, data)

    def insert(self, metadata, data):
        try:
            dao = self.metadata.get('sink')
            db_table = '%s.%s' % (self.metadata.get("database"), self.metadata.get('table'))
            dao().insert(db_table=db_table, dataframe=data)
        except Exception as error: 
            logger.error(error)
  
    @staticmethod
    def build(datasource, metadata):
        return MiddleEntity(source=datasource,
            model=get_model_class(metadata.get('model')),
            field=metadata.get('field'),
            database=metadata.get('database'),
            table=metadata.get('table'),
            embbebedList=metadata.get('embbebedList'),
            options=metadata.get("options"))