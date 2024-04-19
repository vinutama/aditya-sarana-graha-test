# services/logging.py

import logging

CONFIG = {
    "level": logging.INFO,
    "format": "%(asctime)15s | %(name)s/%(levelname)s | %(message)s",
    "handlers": [logging.StreamHandler()],
}


class LoggingService:
    class _LoggingService:
        def __init__(self):
            logging.basicConfig(**CONFIG)
            self.logger = logging.getLogger()

        def get_logger(self):
            return self.logger

    instance = None

    def __init__(self):
        if not LoggingService.instance:
            LoggingService.instance = LoggingService._LoggingService()

    def __getattr__(self, name):
        return getattr(LoggingService.instance, name)
