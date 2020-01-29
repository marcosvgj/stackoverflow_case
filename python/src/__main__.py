import logging
from common.utils.logger import logger
from api.stackoverflow import StackOverflow

log_level = "WARN"
logger.setLevel(getattr(logging, log_level))

if __name__ == '__main__':
    StackOverflow.run()