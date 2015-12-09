import logging
from logging.handlers import RotatingFileHandler


def configure_logger(name, file_name, level):
    log_format = ('%(threadName)s %(asctime)s %(name)s '
                  '%(levelname)s %(message)s')
    handler = RotatingFileHandler(file_name, maxBytes=1024 * 1024, backupCount=30)
    handler.setFormatter(logging.Formatter(log_format))

    task_logger = logging.getLogger(name)
    task_logger.addHandler(handler)
    task_logger.setLevel(level)
