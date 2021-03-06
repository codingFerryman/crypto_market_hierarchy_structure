# Multi-timescale correlation network structures of the cryptocurrency prices

This repository is for the project in the course [Network Science](https://www.ifi.uzh.ch/en/bdlt/Teaching/Network-Science.html)


## File descriptions
|File name|Description|
|---|---|
|[setup_env.sh](./setup_env.sh) | Bash script to perform data download. Please look into the file for its detailed description.|
|[get_coin_code.py](./get_coin_code.py) | The code to obtain the code of coins from Bitfinex. The result is in [cryptocurrency_code.txt](./cryptocurrency_code.txt).|
|[stablecoin.txt](./stablecoin.txt) | The code of stablecoins we considered in the project.|
|[exploration.ipynb](./src/exploration.ipynb) | Data exploration including integrity check, fluctuation investigation, and stablecoin analysis.|
|[crypto_correlation.ipynb](./src/crypto_correlation.ipynb) | It loads data and calculates correlation matrics in different timescales.|
|[community.ipynb](./src/community.ipynb) | The implementation of community analysis. Note: GitHub has rendering error on this file, please download it or take a look at [nbviewer](https://nbviewer.org/github/codingFerryman/crypto_market_hierarchy_structure/blob/main/src/community.ipynb) for a view.|
|[30m_MST_per_day.ipynb](./src/30m_MST_per_day.ipynb) | MST similarity analysis.|
|[MST_series_gif.m](./src/MST_series_gif.m) | MST series animation using MatLab.|
|[graph_generation.ipynb](./src/graph_generation.ipynb) | This is the file for functions that generate networks from matrices by MST and PMFG. |
|[degree_analysis.ipynb](./src/degree_analysis.ipynb) | This is file for functions and part of the resulting figures of degree analysis on cryptocurrency networks. |

## Environment setup
After cloning this repository, please create or activate a virtual environment, then execute:
```bash
cd PATH-TO-REPO-DIR
bash ./setup_env.sh
```

## Data download
Execute from [data_downloader.py](src/data_downloader.py). An example:
```python3
python src/data_downloader.py coin="BTC,ETH,AVAX,SOL,LUNA,LTC,ZEC,TRX,DOT,XRP,CTK" start="2021-01-01" end="2021-11-01" interval="1m"
```
Arguments:
- coin: "code-of-coin(s)", separated by comma(s). 
Codes should exist [here](https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange) as "codeUSD" or "code:USD".
Default by all the coins listed in [cryptocurrency_code.txt](./cryptocurrency_code.txt).
- start: "YYYY-MM-DD", included.
- end: "YYYY-MM-DD", NOT included.
- interval: Select one or more from ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '1W'], separated by comma(s).
- output: (Optional) The path of output file.

Or edit [data_download.sh](./data_download.sh) then execute it.

Note: The downloader will concatenate the existing data with the incoming data. Existing entries with the same timestamps will be updated.

Attention for data attributes change: The code of coins is included in the output files after [commit f72d222](https://github.com/codingFerryman/crypto_market_hierarchy_structure/tree/f72d2225edaabeeee33009772324624339e49b8b), data files downloaded before this commit can be upgraded by downloading any data (with the same coin and interval settings) using the new [data_downloader.py](src/data_downloader.py).



