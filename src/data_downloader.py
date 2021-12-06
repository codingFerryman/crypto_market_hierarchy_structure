import itertools
import logging
import sys
from typing import Tuple
import requests
import ciso8601
import time
from pathlib import Path
import pandas as pd
import math
import ast
from typing import List
from utils import get_logger, timestamp_to_datestring
from tqdm.auto import tqdm

logger = get_logger('downloader', "info")


class DataDownloader(object):
    def __init__(self, symbol, start_timestamp, end_timestamp, save_path):
        """
        Initialization
        :param symbol: the code of a crypto
        :param start_timestamp: the first day (incl.)
        :param end_timestamp: the last day (NOT incl.)
        :param save_path: output path
        """
        self.symbol = symbol
        self.start_timestamp = int(start_timestamp)
        self.end_timestamp = int(end_timestamp)
        self.save_path = save_path

    @staticmethod
    def request_until_success(url, wait_seconds_if_fail=65):
        """
        Download data by HTTPS request
        :param url: requested URL
        :param wait_seconds_if_fail: wait specified seconds if the response is not 200 OK
        :return: raw text
        """
        response = requests.get(url)
        code = response.status_code
        while code != 200:
            logger.error(f'Request failed! Waiting for {wait_seconds_if_fail} seconds ...')
            time.sleep(wait_seconds_if_fail)
            response = requests.get(url)
            code = response.status_code
        _text = response.text
        return _text


class BitfinexDownloader(DataDownloader):
    def __init__(self,
                 coin: str = 'BTC',
                 start_date: str = '20210601',
                 end_date: str = '20210801',  # NOT included!
                 interval: str = '1D',
                 limitation=9995,
                 save_path=None
                 ):
        """
        Data downloader for Bitfinex
        :param coin: the code of a crypto
        :param start_date: the first day (incl.) YYYYMMDD or YYYY-MM-DD
        :param end_date: the last day (NOT incl.) YYYYMMDD or YYYY-MM-DD
        :param interval: i.e. frequency of price changes
        :param limitation: the maximum number of entries per request
        :param save_path: output path
        """
        self.base_url = "https://api-pub.bitfinex.com/v2/"
        self.coin = coin
        symbol = self.convert_coin_to_symbol(coin)
        self.start_date_raw = start_date
        self.end_date_raw = end_date
        start_date = time.mktime(ciso8601.parse_datetime(start_date).timetuple())
        end_date = time.mktime(ciso8601.parse_datetime(end_date).timetuple())

        supported_interval = ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W']
        assert (interval in supported_interval), f"Interval {interval} is not supported."
        self.interval = interval

        self.limitation = limitation

        if save_path is None:
            _save_dir = Path(Path(__file__).parent.resolve(), '..', 'data', interval).resolve()
            if not _save_dir.is_dir():
                _save_dir.mkdir(parents=True, exist_ok=True)
            save_path = Path(_save_dir, f'{symbol}_{interval}.csv')
        super(BitfinexDownloader, self).__init__(symbol, start_date, end_date, save_path)

        self.urls = []
        self.urls_datetime = []

    def _convert_coin_to_symbol(self, coin, pair_currency):
        """
        Check and adapt the input to the supported format
        :param coin: the code of a crypto
        :param pair_currency: fiat currency
        :return: Adapted code
        """
        _text = self.request_until_success('https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange')
        symbol_supported = ast.literal_eval(_text)[0]
        _symbol_1 = coin.upper() + pair_currency.upper()
        _symbol_2 = coin.upper() + ':' + pair_currency.upper()
        if _symbol_1 in symbol_supported:
            return _symbol_1
        elif _symbol_2 in symbol_supported:
            return _symbol_2
        else:
            raise Exception('Coin {coin} or currency {pair_currency} is not supported.')

    def convert_coin_to_symbol(self, coin, pair_currency='USD'):
        """
        Adapt the input to the supported format
        :param coin: the code of a crypto
        :param pair_currency: fiat currency (it only supports USD right now)
        :return: Code for request
        """
        _symbol = self._convert_coin_to_symbol(coin, pair_currency)
        symbol = 't' + _symbol
        return symbol

    def _generate_timestamp_list(self, interval_sec) -> List[Tuple[int, int]]:
        """
        Divide the request to meet the requirement (API limitation)
        :param interval_sec: i.e. frequency of price changes (in seconds)
        :return: list of timestamp ranges
        """
        # Divide the requested date range into _n ranges
        _n = math.ceil(((self.end_timestamp - self.start_timestamp) // interval_sec) / self.limitation)
        logger.debug(f"The requested data has to be downloaded in {_n} requests")
        result = []
        _start = self.start_timestamp
        i = 1
        while i < _n:
            _end = _start + interval_sec * (self.limitation - 1)
            result.append((_start, _end))
            _start = _end + interval_sec
            i += 1
        result.append((_start, self.end_timestamp))
        return result

    def generate_timestamp_list(self):
        """
        Convert the specified interval dates to timestamp
        :return: list of timestamp ranges
        """
        interval_unit = self.interval[-1]
        interval_unit_sec = None
        if interval_unit == 'm':
            interval_unit_sec = 60
        elif interval_unit == 'h':
            interval_unit_sec = 60 * 60
        elif interval_unit == 'D':
            interval_unit_sec = 24 * 60 * 60
        elif interval_unit == 'W':
            interval_unit_sec = 7 * 24 * 60 * 60
        interval_sec = int(self.interval[:-1]) * interval_unit_sec
        if (self.end_timestamp - self.start_timestamp) // interval_sec <= self.limitation:
            logger.debug("The requested data can be downloaded in 1 request")
            return [(self.start_timestamp, self.end_timestamp)]
        else:
            return self._generate_timestamp_list(interval_sec)

    def generate_candle_request_url_list(self) -> List[str]:
        """
        Generate the list of timestamp ranges to URLs
        :return: the list of URLs
        """
        path_params = f"candles/trade:{self.interval}:{self.symbol}/hist"

        timestamp_list = self.generate_timestamp_list()
        query_params_list = []
        for timestamp_tuple in timestamp_list:
            _start_timestamp = int(timestamp_tuple[0] * 1000)
            _end_timestamp = int(timestamp_tuple[1] * 1000)
            query_params = f"?limit={10000}&start={_start_timestamp}&end={_end_timestamp}&sort=1"
            query_params_list.append(query_params)
        for query_params in query_params_list:
            url = self.base_url + path_params + query_params
            self.urls.append(url)

        self.urls_datetime = [
            (timestamp_to_datestring(time_tuple[0] * 1000), timestamp_to_datestring(time_tuple[1] * 1000))
            for time_tuple in timestamp_list]
        return self.urls

    def download_and_save_candle(self):
        """
        Save the downloaded data to a file
        """
        assert (len(self.urls) > 0), "Please generate urls before downloading"
        urls_n = len(self.urls)

        source_col_name = ['timestamp', 'open', 'close', 'high', 'low', 'volume']

        if Path(self.save_path).is_file():
            _tmp_result_df = pd.read_csv(self.save_path, index_col='timestamp')
            if 'coin' not in _tmp_result_df.columns:
                _tmp_result_df['coin'] = self.coin
            result_dict = _tmp_result_df.to_dict('index')
        else:
            result_dict = {}

        _empty_entries_len = 0
        for idx, url in enumerate(self.urls):
            datetime_range = self.urls_datetime[idx]
            logger.debug(
                f"({idx + 1}/{urls_n}) Requesting: {self.symbol} from {datetime_range[0]} to {datetime_range[1]}")
            _tmp_data = ast.literal_eval(self.request_until_success(url))
            _tmp_data = pd.DataFrame(data=_tmp_data, columns=source_col_name)
            _tmp_data['datetime'] = _tmp_data.timestamp.apply(timestamp_to_datestring)
            _tmp_dict = _tmp_data.set_index('timestamp').to_dict('index')
            if len(_tmp_dict) == 0:
                _empty_entries_len += 1
            else:
                result_dict.update(_tmp_dict)

        if _empty_entries_len == len(self.urls):
            logger.warning(f"NO DATA returned: The {self.interval} price of coin {self.coin} "
                           f"from {self.start_date_raw} to {self.end_date_raw}")
            return
        else:
            if _empty_entries_len > 0:
                logger.warning(f"Has MISSING DATA: The {self.interval} price of coin {self.coin} "
                               f"from {self.start_date_raw} to {self.end_date_raw}")
            result_df = pd.DataFrame.from_dict(result_dict, orient='index')
            result_df['coin'] = [self.coin] * len(result_df)
            result_df['timestamp'] = result_df.index
            result_df.set_index(['timestamp', 'coin'], inplace=True)
            result_df = result_df.sort_index()
            result_df.to_csv(self.save_path)
            logger.debug(f"The {self.interval} price of coin {self.coin} "
                         f"from {self.start_date_raw} 00h00m to {self.end_date_raw} 00h00m has been saved to ")
            logger.debug(f"{Path(self.save_path).resolve()}")
            return


def main(args: List[str] = None):
    if args is None:
        argv = {}
    else:
        argv = {a.split('=')[0]: a.split('=')[1] for a in args[1:]}
    coins = argv.get('coin', 'BTC')
    coins_list = coins.split(',')
    start_date = argv.get('start', '20210201')
    end_date = argv.get('end', '20210501')
    intervals = argv.get('interval', '1h')
    intervals_list = intervals.split(',')
    output = argv.get('output', None)

    _zipped_list = list(itertools.product(coins_list, intervals_list))
    logger.info(f"Downloading: {len(coins_list)} coin(s) from {start_date} to {end_date} in {intervals_list} ...")

    for coin, interval in tqdm(_zipped_list) if logger.level != logging.DEBUG else _zipped_list:
        d = BitfinexDownloader(coin=coin, start_date=start_date, end_date=end_date, interval=interval, save_path=output)
        d.generate_candle_request_url_list()
        d.download_and_save_candle()
    logger.info(f"Downloaded!\n")


if __name__ == '__main__':
    main(sys.argv)
    # main()
