from pyspark.sql import SparkSession
from common.utils.utils import get_spark_jar

def getOrCreate():
    return SparkSession.builder\
                .master("local[*]")\
                .appName("Data engineering at Ame Digital")\
                .config("spark.jars", get_spark_jar())\
                .getOrCreate()