#!/usr/bin/bash

# This is an example of executing data_downloader.py
# Supported date format: YYYYMMDD and YYYY-MM-DD
# Supported interval: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W'
# Please be aware that the end date won't be included
python src/data_downloader.py coin="BTC,ETH,AVAX,SOL,LUNA,LTC,ZEC,TRX,DOT,XRP,CTK" start="20210101" end="20211101" interval="1m"
