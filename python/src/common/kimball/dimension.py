from common.utils import spark
from common.ingestor.base import Ingestor
from pyspark.sql.functions import col, explode, split, when, lit


class Dimension(Ingestor):
    def __init__(self, source, model, field, database='default', table='table', sink='HiveDAO', embbebedList=False):
        self.metadata = dict({
            'source': source,
            'database': database,
            'table': table,
            'sink': sink,
            'model': model,
            'embbebedList': embbebedList,
            'description_field': field})

    def save(self):
        data = Ingestor.apply(Dimension.rule, self.metadata)
        self.load(self.metadata, data)

    @staticmethod
    def checkConstraint(field, dataframe):
        """ Responsible for verifying the field's integrity given dataframe"""
        return dataframe.\
            withColumn(field, when(col(field).isNull(), lit('Not Specified'))\
            .otherwise(col(field)))
    
    @staticmethod
    def create_index(field, source):
        return map(lambda x, y: (x, y.asDict()[field]), range(1, len(source)), source)

    @staticmethod
    def rule(metadata):
        """ Responsible to implement business logic to dimensional tables """
        model = metadata.get('model')
        field = metadata.get('description_field')

        if metadata.get('embbebedList') == False:
            data = Dimension.checkConstraint(field=field, dataframe=metadata.get('source'))\
                .select(field)\
                .distinct()\
                .collect()
        else:
            data = Dimension.checkConstraint(field=field, dataframe=metadata.get('source'))\
                .select(field)\
                .withColumn(field, split(col(field), ';'))\
                .withColumn(field, explode(col(field)))\
                .distinct()\
                .collect()

        return spark.getOrCreate().createDataFrame(Dimension.create_index(field, data), model().schema)

    @staticmethod
    def build(datasource, metadata):
        return Dimension(source=datasource,
            model=metadata.get('model'),
            field=metadata.get('field'),
            database=metadata.get('database'),
            table=metadata.get('table'),
            embbebedList=metadata.get('embbebedList'),
            sink=metadata.get('sink'))

