from common.utils import spark
from common.base_dao.base import DAO
from common.utils.logger import logger 
from common.utils.reader import configuration

class PostgresDAO(DAO):
    def __init__(self):
        """API to access Postgres RDBMS - DAO Implementation"""
        secret = configuration()
        self.host = secret.get('postgres').get('host')
        self.database = secret.get('postgres').get('database')
        self.user = secret.get('postgres').get('user')
        self.password = secret.get('postgres').get('password')
        self.port = secret.get('postgres').get('port')
        
    def select(self, db_table):
        """Query engine to this DAO implementation"""
        try:
            return spark.getOrCreate().read\
            .format('jdbc')\
            .option('url', "jdbc:postgresql://%s:%s/%s" % (self.host, self.port, self.database))\
            .option('dbtable', db_table)\
            .option('user', self.user)\
            .option('password', self.password)\
            .option('driver', 'org.postgresql.Driver')\
            .load()     
        except Exception as error: 
            logger.error(error)
            
    def insert(self, db_table, dataframe):
        """Data ingestion engine to this DAO implementation"""
        try:
            dataframe.write\
            .format('jdbc')\
            .option('url', "jdbc:postgresql://%s:%s/%s" % (self.host, self.port, self.database))\
            .option('dbtable', db_table)\
            .option('user', self.user)\
            .option('password', self.password)\
            .option('driver', 'org.postgresql.Driver')\
            .mode('append')\
            .save()
        except Exception as error: 
            logger.error(error)