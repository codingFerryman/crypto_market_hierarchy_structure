import requests
import time
import ast
url = "https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange"
response = requests.get(url)
code = response.status_code
while code != 200:
    time.sleep(70)
    response = requests.get(url)
    code = response.status_code

text = response.text
symbols = ast.literal_eval(text)[0]
coins = []
for coin in symbols:
    if coin[-4:] == ':USD':
        coins.append(coin[:-4])
    elif coin[-3:] == 'USD':
        if coin[-7:] != 'TESTUSD':
            coins.append(coin[:-3])

with open('./cryptocurrency_code.txt', 'w') as fp:
    fp.write(',\n'.join(coins))

