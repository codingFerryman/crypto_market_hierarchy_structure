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
Execute from [data_downloader.py](./data_downloader.py). An example:
```python3
python data_downloader.py coin="BTC,ETH,AVAX,SOL,LUNA,LTC,ZEC,TRX,DOT,XRP,CTK" start="20210101" end="20211101" interval="1m"
```

Or edit the [data_download.sh](./data_download.sh) then execute it.
