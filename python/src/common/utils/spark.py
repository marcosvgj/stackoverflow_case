from pyspark.sql import SparkSession
from functools import lru_cache

@lru_cache(maxsize=None)
def getOrCreate():
    return SparkSession.builder\
                .master("local[*]")\
                .appName("Data engineering at Ame Digital")\
                .getOrCreate()
                #.config("spark.jars", "/home/marcos/dataengineeringatame/python/jars/postgresql-42.2.9.jre6.jar")\