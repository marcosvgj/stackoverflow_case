from pyspark.sql.types import StructField, StringType, IntegerType, StringType, StructType

class CommunicationToolModel:
    @property
    def schema(self):    
        return StructType([
            StructField('ferramenta_comunic_id', IntegerType(), False),
            StructField('nome', StringType(), False)])

class SOModel(StructType):
    @property
    def schema(self):
        return StructType([
                    StructField('sistema_operacional_id', IntegerType(), False),
                    StructField('nome', StringType(), False)])
    
class LanguageWorkedWithModel:
    @property
    def schema(self):    
        return StructType([
            StructField('linguagem_programacao_id', IntegerType(), False),
            StructField('nome', StringType(), False)])
    
class CompanyModel:
    @property
    def schema(self):    
        return StructType([
            StructField('empresa_id', IntegerType(), False),
            StructField('tamanho', StringType(), False)])

class CountryModel:
    @property
    def schema(self):    
        return StructType([
            StructField('pais_id', IntegerType(), False),
            StructField('nome', StringType(), False)])