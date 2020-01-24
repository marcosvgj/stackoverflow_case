import logging
from common.utils.logger import logger
from api.stackoverflow import Entrypoint
from common.utils.spark import getOrCreate
from common.utils.reader import configuration
from dao.postgres.dao import PostgresDAO

log_level = "WARN"

def main():
    logger.setLevel(getattr(logging, log_level))
    """ Entrypoint to spark job """
    ingestor = Entrypoint()
    ingestor.run()

if __name__ == '__main__':
    main()