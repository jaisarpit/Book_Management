# logger.py
import logging
from logging.handlers import RotatingFileHandler
from flask import g

def setup_logger(request_id=None):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logger's level to DEBUG

    # Create a file handler and set its level to DEBUG
    file_handler = RotatingFileHandler('app.log', maxBytes=1024000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(request_id)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Add the request ID to the logger's extra context
    extra = {'request_id': request_id}
    logger = logging.LoggerAdapter(logger, extra)

    return logger
