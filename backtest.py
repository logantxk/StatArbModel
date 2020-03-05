import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
from datetime import datetime

# read in the prices from csv
data = pd.read_csv("BinancePrices.csv")
print(data.head())

# Top cryptos in analysis were LTC/EOS, XLM/XRP, ETH/LTC, ETH/NEO, ADA/XLM
cryptoOne = 'LTC'
cryptoTwo = 'EOS'


# Trade using a simple strategy
def trade(S1, S2, window1, window2):
    # If window length is 0, algorithm doesn't make sense, so exit
    if (window1 == 0) or (window2 == 0):
        return 0

    # Compute rolling mean and rolling standard deviation
    ratios = S1 / S2
    ma1 = ratios.rolling(window=window1,
                         center=False).mean()
    ma2 = ratios.rolling(window=window2,
                         center=False).mean()
    std = ratios.rolling(window=window2,
                         center=False).std()
    zscore = (ma1 - ma2) / std

    # Simulate trading
    # Start with no money and no positions
    day = 0
    money = 0
    countS1 = 0
    countS2 = 0
    for i in range(len(ratios)):
        # Sell short if the z-score is > 1
        if zscore[i] > 1:
            money += S1[i] - S2[i] * ratios[i]
            countS1 -= 1
            countS2 += ratios[i]
            day += 1
            print("Day:", day)
            print('Sell %s Long %s' % (cryptoOne, cryptoTwo))
            print('Selling Ratio %s %s %s %s' % (money, ratios[i], countS1, countS2),'\n')
        # Buy long if the z-score is < 1
        elif zscore[i] < -1:
            money -= S1[i] - S2[i] * ratios[i]
            countS1 += 1
            countS2 -= ratios[i]
            day += 1
            print("Day:", day)
            print('Long %s Sell %s' % (cryptoOne, cryptoTwo))
            print('Buying Ratio %s %s %s %s' % (money, ratios[i], countS1, countS2),'\n')
        # Clear positions if the z-score between -.5 and .5
        elif abs(zscore[i]) < 0.75:
            money += S1[i] * countS1 + S2[i] * countS2
            countS1 = 0
            countS2 = 0
            day += 1
            print("Day:", day)
            print('Exit pos %s %s %s %s' % (money, ratios[i], countS1, countS2), '\n')
        else:
            day += 1
            print("Day:",day)
            print("Do nothing \n")

    # Close out final position
    money += S1[i] * countS1 + S2[i] * countS2
    countS1 = 0
    countS2 = 0
    day += 1
    print("Final Closing")
    print('Exit pos %s %s %s %s' % (money, ratios[i], countS1, countS2), '\n')
    print("Money made/lost", money)
    return money

# You can also alter the z-score trade signals inside the trade function
# trade inputs the two cryptos and the rolling average windows in days which calculates z-scores
trade(data[cryptoOne], data[cryptoTwo], 5, 30)