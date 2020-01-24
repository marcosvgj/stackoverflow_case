from common.utils import spark
from common.ingestor.base import Ingestor
from pyspark.sql.functions import col, explode, split, when, lit


class Fact(Ingestor):
    def __init__(self, source, model, field, database='default', table='table', sink='HiveDAO', embbebedList=False):
        self.metadata = dict({
            'source': source,
            'database': database,
            'table': table,
            'sink': sink,
            'model': model,
            'description_field': field})

    def save(self):
        data = Ingestor.apply(Fact.rule, self.metadata)
        self.load(self.metadata, data)

    @staticmethod
    def rule(metadata):
        """TODO"""
