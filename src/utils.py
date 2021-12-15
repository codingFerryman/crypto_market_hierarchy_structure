from sklearn.preprocessing import MinMaxScaler
from typing import List
import logging
from pathlib import Path
import pytz
import coloredlogs
import datetime
import ciso8601
import pandas as pd
import numpy as np

date_string_format = '%Y-%m-%d %H:%M:%S'


def check_integrity(start_from, end_before, csv_file, interval=None):
    """
    Check the integrity of a datafile
    :param start_from: YYYY-MM-DD the start date
    :param end_before: YYYY-MM-DD the end date
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


def check_integrity_score(start_from, end_before, coins, data_dir='./data', check_intervals=['3h', '30m']):
    """
    Calculate integrity score for each coin
    :param start_from: YYYY-MM-DD the start date, or a timestamp
    :param end_before: YYYY-MM-DD the end date, or a timestamp
    :param coins: list of coin codes
    :param data_dir: the path of data directory
    :param check_intervals: list of intervals
    :return: dict of scores
    """
    _coins_integrity = {}
    for _interval in check_intervals:
        _coins_integrity[_interval] = {}
        _data_interval_dir = Path(data_dir, _interval)
        for _coin in coins:
            _file_path = Path(_data_interval_dir, f"{_coin}_USD_{_interval}.csv")
            _c_df = load_data(start_from, end_before, _file_path, fill_na=True)
            _coins_integrity[_interval][_coin] = len(_c_df[_c_df.is_fill == False]) / len(_c_df)
        print(f"The integrity score of {_interval} data: {np.mean(list(_coins_integrity[_interval].values()))}")
    return _coins_integrity


def get_sorted_fluctuation_coins(start_from, end_before,
                                 data_dir,
                                 normalize_price: bool = False,
                                 incl_coins: List = None,
                                 return_details: bool = False,
                                 **kwargs):
    """
        start_from (str, int): the timestamp or datestring of the first day
        end_before (str, int): the timestamp or datestring of the last day
        data_dir   (str):   the path if directory which has .csv files
        normalize_price (bool): use MinMaxScaler() to normalize the close price if True
        incl_coins (list, None): only return the coins in this provided list; None to return all coins
        return_details (bool): return the standard deviations in a DataFrame if True; False to only return a list with coin codes
        [DEPRECATED] start_from_timestamp (int): the timestamp of the first day
        [DEPRECATED] end_before_timestamp (int): the timestamp of the last day
    )
    """
    _coins_df_list = []
    _coins_path_list = [p for p in Path(data_dir).iterdir() if p.suffix == '.csv']
    for coin_path in _coins_path_list:
        _coins_df_list.append(load_data(start_from, end_before, coin_path, fill_na=False, price='close'))
    coins_df = pd.concat(_coins_df_list)
    if incl_coins is not None:
        coins_df = coins_df[coins_df.index.isin(incl_coins, level='coin')]
    if normalize_price:
        _normalized_df_list = []
        for coin in coins_df.index.get_level_values('coin'):
            scaler = MinMaxScaler()
            _tmp_df = coins_df[coins_df.index.get_level_values('coin') == coin].copy()
            _tmp_df['close'] = scaler.fit_transform(_tmp_df[['close']])
            _normalized_df_list.append(_tmp_df)
        coins_df = pd.concat(_normalized_df_list)
    coins_df = coins_df.drop('is_fill', axis=1)
    std_df = coins_df.groupby('coin').agg(
        {
            'close': 'std',
            'volume': 'sum'
        }
    )
    std_df = std_df.rename(columns={'close': 'close_std', 'volume': 'volume_sum'})
    result = std_df.sort_values('close_std', ascending=False, axis=0)
    if return_details:
        return result
    else:
        return result.index.to_list()


def load_data(start_from, end_before, file_path, fill_na=False, price='close', interval=None, **kwargs):
    start_from_timestamp, end_before_timestamp = _adapt_input(start_from=start_from, end_before=end_before, **kwargs)
    prices = ['open', 'close', 'high', 'low']
    select_prices = price.split(',')
    remove_prices = list(set(prices) - set(select_prices))
    if interval is None:
        interval = Path(file_path).stem.split('_')[-1]
    data_df = pd.read_csv(file_path).set_index(["timestamp", "coin"])
    if (start_from_timestamp is not None) and (end_before_timestamp is not None):
        data_df = data_df.loc[start_from_timestamp:end_before_timestamp]
    else:
        start_from_timestamp = min(
            data_df.index.get_level_values(level='timestamp')) if start_from_timestamp is None else start_from_timestamp
        end_before_timestamp = max(
            data_df.index.get_level_values(level='timestamp')) if end_before_timestamp is None else end_before_timestamp
    data_df['datetime'] = data_df.index.get_level_values('timestamp').map(timestamp_to_datetime)
    data_df = data_df.drop(columns=remove_prices)
    data_df['is_fill'] = False
    if fill_na and len(data_df) > 0:
        golden_timestamps = get_golden_timestamps(start_from_timestamp, end_before_timestamp, interval)
        data_df = my_fillna(data_df, golden_timestamps, select_prices)
    return data_df


def _adapt_input(**kwargs):
    start_from = kwargs.get('start_from', None)
    end_before = kwargs.get('end_before', None)
    start_from_timestamp = kwargs.get('start_from_timestamp', None)
    end_before_timestamp = kwargs.get('end_before_timestamp', None)
    if start_from_timestamp is None and start_from:
        if type(start_from) is str:
            start_from_timestamp = datestring_to_timestamp(start_from)
        else:
            start_from_timestamp = start_from
    if end_before_timestamp is None and end_before:
        if type(end_before) is str:
            end_before_timestamp = datestring_to_timestamp(end_before)
        else:
            end_before_timestamp = end_before
    return start_from_timestamp, end_before_timestamp


def get_golden_timestamps(start_from, end_before, interval, **kwargs):
    start_from_timestamp, end_before_timestamp = _adapt_input(start_from=start_from, end_before=end_before, **kwargs)
    interval_ms = interval_to_ms(interval)
    golden_timestamps = []
    _timestamp = start_from_timestamp
    while _timestamp <= end_before_timestamp:
        golden_timestamps.append(_timestamp)
        _timestamp += interval_ms
    return golden_timestamps


def datestring_to_timestamp(datestring):
    return int(ciso8601.parse_datetime(datestring + "T00:00:00Z").timestamp() * 1000)


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
