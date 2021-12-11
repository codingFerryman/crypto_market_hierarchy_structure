import logging
from pathlib import Path
import pytz
import coloredlogs
import datetime
import time
import ciso8601
import pandas as pd

date_string_format = '%Y-%m-%d %H:%M:%S'


def check_integrity(start_from, end_before, csv_file, interval=None):
    """
    Check the integrity of a datafile
    :param start_from: YYYYMMDD the start date
    :param end_before: YYYYMMDD the end date
    :param csv_file: data csv file path
    :param interval: default by the interval in the filename
    :return: return the complete data in the given period, or None
    """
    integrity_flag = False
    start_timestamp = datestring_to_timestamp(start_from)
    end_timestamp = datestring_to_timestamp(end_before)
    data_df = pd.read_csv(csv_file).set_index(["timestamp", "coin"])
    if interval is None:
        interval = Path(csv_file).stem.split('_')[-1]
    if interval == '1W':
        start_date = timestamp_to_datetime(start_timestamp)
        end_date = timestamp_to_datetime(end_timestamp)
        start_weekday = start_date.isoweekday()
        end_weekday = end_date.isoweekday()
        if start_weekday != 1:
            start_date += datetime.timedelta(days=8 - start_weekday)
            start_timestamp = int(start_date.timestamp()) * 1000
        if end_weekday != 1:
            end_date += datetime.timedelta(days=1 - end_weekday)
            end_timestamp = int(end_date.timestamp()) * 1000

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


def load_data(start_from_timestamp, end_before_timestamp, file_path, fill_na=False, price='close', interval=None):
    prices = ['open', 'close', 'high', 'low']
    select_prices = price.split(',')
    remove_prices = list(set(prices) - set(select_prices))
    if interval is None:
        interval = Path(file_path).stem.split('_')[-1]
    data_df = pd.read_csv(file_path).set_index(["timestamp", "coin"])
    data_df = data_df.loc[start_from_timestamp:end_before_timestamp]
    data_df['datetime'] = data_df.index.get_level_values('timestamp').map(timestamp_to_datetime)
    data_df = data_df.drop(columns=remove_prices)
    data_df['is_fill'] = False
    if fill_na:
        golden_timestamps = get_golden_timestamps(start_from_timestamp, end_before_timestamp, interval)
        data_df = my_fillna(data_df, golden_timestamps, select_prices)
    return data_df


def get_golden_timestamps(start_from_timestamp, end_before_timestamp, interval):
    interval_ms = interval_to_ms(interval)
    golden_timestamps = []
    _timestamp = start_from_timestamp
    while _timestamp <= end_before_timestamp:
        golden_timestamps.append(_timestamp)
        _timestamp += interval_ms
    return golden_timestamps


def datestring_to_timestamp(datestring):
    return int(ciso8601.parse_datetime(datestring+"T00:00:00Z").timestamp() * 1000)


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp) / 1000.0).astimezone(pytz.utc)


def my_fillna(one_coin_data_df, golden_timestamps, fill_col):
    check_coin = set(one_coin_data_df.index.get_level_values("coin")).pop()
    df_for_check = pd.DataFrame({"timestamp": golden_timestamps, "coin": check_coin}).set_index(["timestamp", "coin"])
    joined_check_df = df_for_check.join(one_coin_data_df)
    joined_check_df['datetime'] = df_for_check.index.get_level_values('timestamp').map(timestamp_to_datetime)
    fill_col.append('volume')
    for col in fill_col:
        joined_check_df[col] = joined_check_df[col].interpolate()
        joined_check_df['is_fill'] = joined_check_df['is_fill'].fillna(True)
    return joined_check_df




def timestamp_to_datestring(timestamp):
    date = timestamp_to_datetime(timestamp)
    datestring = date.strftime(date_string_format)
    return datestring


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
