import logging
from common.utils.logger import logger
from common.utils.spark import getOrCreate
from common.utils.reader import configuration
from service.stackoverflow import Pipeline

log_level = "WARN"
logger.setLevel(getattr(logging, log_level))

def main():
    pipeline = Pipeline()
    pipeline.run()

if __name__ == '__main__':
    main()