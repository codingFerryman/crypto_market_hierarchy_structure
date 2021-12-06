#!/usr/bin/bash

# This is an example of executing data_downloader.py
# Supported date format: YYYYMMDD and YYYY-MM-DD
# Supported interval: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W'
# Please be aware that the end date won't be included

# All codes
CODES=$(tr -d "\n\r" < cryptocurrency_code.txt)

# Download
python src/data_downloader.py \
coin=$CODES \
start="2021-01-13" \
end="2021-03-14" \
interval="1W" \
# output="./output.csv"
