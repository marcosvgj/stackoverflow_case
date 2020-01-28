from pyspark.sql.functions import col, explode, split, when, lit
from pyspark.sql.window import Window  

"""
TODO:
     - Tornar parametrizável a geração da tabela
     - Verificar se campo alvo utiliza estruturas ArrayType()
     - Indexar e ingerir os dados    
     - Segregação das regras de negócio
     - Refatorar código da geração Entidade Intermediaria
"""
class IntermediaryEntity(Ingestor):
    def __init__(self, source, model, field, options, database='default', table='table', sink='HiveDAO',
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

    def save(self):
        data = Ingestor.apply(IntermediaryEntity.rule, self.metadata)
        self.load(self.metadata, data)

    def get(self):
        return Ingestor.apply(IntermediaryEntity.rule, self.metadata)

    @staticmethod
    def checkConstraint(field, dataframe):
        """ Responsible for verifying the field's integrity given dataframe"""
        return dataframe.\
            withColumn(field, when(col(field).isNull(), lit('Not Specified'))\
            .otherwise(col(field)))
    
    @staticmethod
    def create_index(columns, source):
        return map(lambda x, y: (x, y.asDict()[columns]), range(1, len(source)), source)
    
    @staticmethod
    def createIndex(ordered_column, index, source):
        w = Window.orderBy(asc(ordered_column))
        return source.withColumn(index, row_number().over(w))
    
    @udf()
    def conversor(field):
        try:
            return MAPPER.value[field]
        except KeyError as err:
            return field
    
    @staticmethod
    def rule(metadata):
        """ Responsible to implement business logic to dimensional tables """
        model = metadata.get('model')
        options = metadata.get('options')
        field = metadata.get('description_field')
        table = options.get('relationTable')
        database = options.get("relationDatabase")
        print(options.get("originalColumn"))
        dimension = PostgresDAO().select(f'{database}.{table}')
        
        if metadata.get('embbebedList') == False:
            data = Dimension.checkConstraint(field=field, dataframe=metadata.get('source'))\
                .select(options.get('intermediaryColumns'))\
                .join(dimension, col(options.get('originalColumn')) == getattr(dimension, \
                                                                                   options.get("dimensionalColumn")))
            data = data.withColumnRenamed(options.get('relationTableId'), options.get('relationTableId'))
            return IntermediaryEntity.createIndex(options.get('originalIdColumn'), options.get('relationTbID'), data)
            
            #return data.select(model().schema.fieldNames())
            
            
        else:
            data = Dimension.checkConstraint(field=field, dataframe=metadata.get('source'))\
                .select(options.get('intermediaryColumns'))\
                .withColumn(field, split(col(options.get("originalColumn")), ';'))\
                .withColumn(field, explode(col(options.get("originalColumn"))))\
                .join(dimension, col(options.get('originalColumn')) == getattr(dimension, \
                                                                                   options.get("dimensionalColumn")))
            data = data.withColumnRenamed(options.get('originalIdColumn'), options.get('relationTableId'))
            data = data.withColumn(options.get('relationTableId'), col(options.get('relationTableId')).cast(IntegerType()))
            data = IntermediaryEntity.createIndex(options.get('relationTableId'), options.get('relationTbID'), data)
            if options.get("hasAdicionalColumns") == True:
                for i in options.get("adicionalColumns"):
                    setup = options.get("adicionalColumnsMapper")[i]
                    data = data.withColumnRenamed(i, setup["name"])
                    if setup.get("hasValueConversion") == True:
                        global MAPPER
                        MAPPER = spark.sparkContext.broadcast(setup["valuesConversor"])
                        data = data.withColumn(setup['name'], IntermediaryEntity.conversor(setup['name']))
                        #MAPPER.destroy()
                    data = data.withColumn(setup['name'], col(setup['name']).cast(setup['type']))
            return data.select(model().schema.fieldNames())
        
    @staticmethod
    def build(datasource, metadata):
        return IntermediaryEntity(source=datasource,
            model=metadata.get('model'),
            field=metadata.get('field'),
            database=metadata.get('database'),
            table=metadata.get('table'),
            embbebedList=metadata.get('embbebedList'),
            sink=metadata.get('sink'),
            options=metadata.get("options"))