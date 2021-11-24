This repository is for the project in the course [Network Science](https://www.ifi.uzh.ch/en/bdlt/Teaching/Network-Science.html)

This project is still in progress.


## Setup
After cloning this repository, please create or activate a virtual environment, then execute:
```bash
cd PATH-TO-REPO-DIR
bash ./setup_env.sh
```

## Execution
### Download data
Execute from [data_downloader.py](src/data_downloader.py). An example:
```python3
python src/data_downloader.py coin="BTC,ETH,AVAX,SOL,LUNA,LTC,ZEC,TRX,DOT,XRP,CTK" start="20210101" end="20211101" interval="1m"
```
Arguments:
- coin: "code-of-coin(s)", separated by comma(s). Codes should exist [here](https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange) as "codeUSD" or "code:USD".
- start: "YYYYMMDD" or "YYYY-MM-DD", included.
- end: "YYYYMMDD" or "YYYY-MM-DD", NOT included.
- interval: One of ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W']

Or edit [data_download.sh](./data_download.sh) then execute it.

Note: The downloader will concatenate the existing data with the incoming data. Existing entries with the same timestamps will be updated.
