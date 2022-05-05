#!/usr/bin/env python3

import time
from Brokers.InteractiveBrokers.dataFarm import *
from Brokers.InteractiveBrokers.marketOrders import *

def testHeikinAshi(IBClient):
    haClose = 0
    haOpen = 0

    try:
        while True:
            if isinstance(IBClient.nextorderId, int):
                getCandles(IBClient, "1 D", "30 mins", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))
                while (IBClient.historicalDataEndStatus == False):
                    pass
                marketData = IBClient.historicalDataArray
                for i in range(0,len(marketData)):
                    if i == 0:
                        haOpen = (marketData[i]["Open"])
                    else:
                        haOpen = (haOpen + haClose) / 2

                    haClose = (marketData[i]["Open"] + marketData[i]["High"] + marketData[i]["Low"] + marketData[i]["Close"]) / 4

                    print(marketData[i]["Date"] + " HAOpen: " + str(haOpen) + " HAClose: " + str(haClose))

            time.sleep(3)
    except Exception as e:
        print(e)

