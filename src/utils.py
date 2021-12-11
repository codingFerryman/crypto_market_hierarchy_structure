import logging
from pathlib import Path

import coloredlogs
import datetime
import time
import ciso8601
import pandas as pd

date_string_format = '%Y-%m-%d %H:%M:%S'


def check_integrity(start_at, end_before, csv_file, interval=None):
    """
    Check the integrity of a datafile
    :param start_at: YYYYMMDD the start date
    :param end_before: YYYYMMDD the end date
    :param csv_file: data csv file path
    :param interval: default by the interval in the filename
    :return: return the complete data in the given period, or None
    """
    integrity_flag = False
    start_timestamp = datestring_to_timestamp(start_at)
    end_timestamp = datestring_to_timestamp(end_before)
    data_df = pd.read_csv(csv_file).set_index("timestamp")
    if interval is None:
        interval = Path(csv_file).stem.split('_')[-1]
    interval_ms = interval_to_ms(interval)
    golden_num = 1 + (end_timestamp - start_timestamp) // interval_ms
    if (start_timestamp in data_df.index) and (end_timestamp in data_df.index):
        data_select = data_df.loc[start_timestamp:end_timestamp]
        entry_num = len(data_select)
        integrity_flag = (golden_num == entry_num)
    if integrity_flag:
        return data_select
    else:
        return None


def timestamp_to_datestring(timestamp):
    date = datetime.datetime.fromtimestamp(float(timestamp) / 1000.0)
    datestring = date.strftime(date_string_format)
    return datestring


def datestring_to_timestamp(datestring):
    return int(time.mktime(ciso8601.parse_datetime(datestring).timetuple()) * 1000)


def interval_to_ms(interval: str):
    interval_unit = interval[-1]
    if interval_unit == 'm':
        interval_unit_sec = 60
    elif interval_unit == 'h':
        interval_unit_sec = 60 * 60
    elif interval_unit == 'D':
        interval_unit_sec = 24 * 60 * 60
    elif interval_unit == 'W':
        interval_unit_sec = 7 * 24 * 60 * 60
    else:
        raise NotImplementedError
    interval_ms = int(interval[:-1]) * interval_unit_sec * 1000
    return interval_ms


def get_logger(name: str, level='info'):
    fmt = '\n[%(asctime)s] - %(name)s - {line:%(lineno)d} %(levelname)s - %(message)s'
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
