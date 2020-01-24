from common.utils.logger import *
from api.stackoverflow import Entrypoint
from common.utils.spark import getOrCreate

log_level = "WARN"
spark = getOrCreate()

def main():
    logger.setLevel(getattr(logging, log_level))
    """ Entrypoint to spark job """
    ingestor = Entrypoint()
    ingestor.run()

import os 

if __name__ == '__main__':
    print(os.getcwd())
    main()