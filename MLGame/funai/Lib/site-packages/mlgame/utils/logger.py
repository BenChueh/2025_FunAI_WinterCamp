import sys
from functools import cache

import loguru

_logger = None


@cache
def get_singleton_logger():
    global _logger
    if _logger is None:
        # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        _logger = loguru.logger

        _logger.remove()
        _logger.add(sys.stdout, level="WARNING")
        # _logger.add(
        #     ".debug.log",
        #     level="DEBUG",
        #     rotation="10 MB",  # Rotate after the log file reaches 10 MB
        #     retention=1,  # Keep only the most recent rotated log file
        #     compression=None  # Do not compress the log file
        # )
    return _logger


logger = get_singleton_logger()
