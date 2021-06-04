import logging
from utils.logger.logger import LoggingMixin

logging.basicConfig(level=logging.INFO,
                    # filename='myapp.log',
                    # filemode='w',
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s')

__ALL__ = [LoggingMixin]