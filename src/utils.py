import logging
import coloredlogs
import datetime


def timestamp_to_datestring(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    datestring = date.strftime('%Y-%m-%d %H:%M:%S')
    return datestring


def get_logger(name: str, level='debug'):
    fmt = '[%(asctime)s] - %(name)s - {line:%(lineno)d} %(levelname)s - %(message)s'
    logger = logging.getLogger(name=name)
    if level.lower() == 'debug':
        logger.setLevel(logging.DEBUG)
        coloredlogs.install(fmt=fmt, level='DEBUG', logger=logger)
    elif level.lower() == 'info':
        logger.setLevel(logging.INFO)
        coloredlogs.install(fmt=fmt, level='INFO', logger=logger)
    elif level.lower() in ['warn', 'warning']:
        logger.setLevel(logging.WARNING)
        coloredlogs.install(fmt=fmt, level='WARNING', logger=logger)
    return logger
