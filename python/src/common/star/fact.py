
from model.models import *
from dao.postgres import PostgresDAO
from common.utils.logger import logger
from common.ingestor.base import Ingestor
from common.utils.utils import get_model_class
from business.rules import FactRules

class Fact(Ingestor):
    def __init__(self, source, model, database='default', table='table', sink=PostgresDAO):
        self.metadata = dict({
            'source': source,
            'database': database,
            'table': table,
            'sink': sink,
            'model': model})

    def get(self):
        self.update_source(Ingestor.apply(FactRules.salary_standardization, self.metadata))
        self.update_source(Ingestor.apply(FactRules.respondent_name_creation, self.metadata))
        self.update_source(Ingestor.apply(FactRules.columns_renames, self.metadata))
        self.update_source(Ingestor.apply(FactRules.treat_embbebed_list, self.metadata))
        self.update_source(Ingestor.apply(FactRules.fact_enrichment, self.metadata))
        self.update_source(Ingestor.apply(FactRules.field_to_boolean, self.metadata))
        return self.filter_schema()
    
    def save(self):
        data = self.get()
        self.insert(metadata=self.metadata, data=data)

    def insert(self, metadata, data):
        try:
            dao = self.metadata.get('sink')
            db_table = '%s.%s' % (self.metadata.get("database"), self.metadata.get('table'))
            dao().insert(db_table=db_table, dataframe=data)
        except Exception as error: 
            logger.error(error)
    
    def update_source(self, data):
        self.metadata.update({'source': data})
    
    def filter_schema(self):
        model = self.metadata.get('model')
        return self.metadata.get('source').select(model().schema.fieldNames()).distinct()

    @staticmethod
    def build(datasource, metadata):
        return Fact(source=datasource,
            model=get_model_class(metadata.get('model')),
            database=metadata.get('database'),
            table=metadata.get('table'))

        
    