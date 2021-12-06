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
- coin: "code-of-coin(s)", separated by comma(s). 
Codes should exist [here](https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange) as "codeUSD" or "code:USD".
Default by all the coins listed in [cryptocurrency_code.txt](./cryptocurrency_code.txt).
- start: "YYYYMMDD" or "YYYY-MM-DD", included.
- end: "YYYYMMDD" or "YYYY-MM-DD", NOT included.
- interval: Select one or more from ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W'], separated by comma(s).
- output: (Optional) The path of output file.

Or edit [data_download.sh](./data_download.sh) then execute it.

Note: The downloader will concatenate the existing data with the incoming data. Existing entries with the same timestamps will be updated.

Attention for data attributes change: The code of coins is included in the output files after [commit f72d222](https://github.com/codingFerryman/crypto_market_hierarchy_structure/tree/f72d2225edaabeeee33009772324624339e49b8b), data files downloaded before this commit can be upgraded by downloading any data (with the same coin and interval settings) using the new [data_downloader.py](src/data_downloader.py).



