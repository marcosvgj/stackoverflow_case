import logging
from common.utils.logger import logger
from api.stackoverflow import Pipeline
from common.utils.spark import getOrCreate
from common.utils.reader import configuration
from dao.postgres.dao import PostgresDAO

log_level = "WARN"
logger.setLevel(getattr(logging, log_level))

def main():
    #pipeline = Pipeline()
    #pipeline.run()
    PostgresDAO().select("stackoverflow.empresa").show(100,False)

if __name__ == '__main__':
    main()


            
