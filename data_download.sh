#!/usr/bin/bash

# This is an example of executing data_downloader.py
# Supported date format: YYYY-MM-DD
# Supported interval: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W'
# Please be aware that the end date won't be included

# All codes
CODES=$(tr -d "\n\r" < cryptocurrency_code.txt)

# Intervals
INTERVALS="5m"

# Download
python src/data_downloader.py \
coin=$CODES \
start="2021-01-10" \
end="2021-03-15" \
interval=$INTERVALS

python src/data_downloader.py \
coin=$CODES \
start="2021-08-14" \
end="2021-10-18" \
interval=$INTERVALS



