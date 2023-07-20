import logging
import sys


class MyLogger:
    def __init__(self, log_file, module_name, logging_enabled=True):
        self.log_file = log_file
        self.module_name = module_name
        self.logging_enabled = logging_enabled
        self._setup_logger()

    def _setup_logger(self):
        if self.logging_enabled:
            logging.basicConfig(
                filename=self.log_file,
                level=logging.INFO,
                format='%(''message)s'
                #'%(levelname)s - %(name)s - %(lineno)d - %('
                #'message)s'
            )
        self.logger = logging.getLogger(self.module_name)

    def enable_logging(self):
        self.logging_enabled = True
        self._setup_logger()

    def disable_logging(self):
        self.logging_enabled = False
        self.logger.handlers = []









