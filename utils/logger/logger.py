import logging


class LoggingMixin:
    def __getattr__(self, name):
        if name in ['critical', 'error', 'warning', 'info', 'debug']:
            if not hasattr(self.__class__, '__logger'):
                self.__class__.__logger = logging.getLogger(f"{self.__class__.__module__}")
            return getattr(self.__class__.__logger, name)
        # return super(LoggingMixin, self).__getattr__(name)

    @staticmethod
    def _get_logger(cls):
        return logging.getLogger(f"{cls.__module__}")

