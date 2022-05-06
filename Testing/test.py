#!/usr/bin/env python3

import time
from math import ceil
from Brokers.InteractiveBrokers.dataFarm import *
from Brokers.InteractiveBrokers.marketOrders import *

def calculateHeikinAshi(IBClient, marketData, DEBUG=False):
    haOpen = 0
    haClose = 0
    stochastic = 0

    HAData = []

    try:
        for i in range(0, len(marketData) - 1):
            if i == 0:
                haOpen = round(marketData[i]["Open"], 2)
            else:
                haOpen = round((haOpen + haClose) / 2, 2)

            haClose = round((marketData[i]["Open"] + marketData[i]["High"] + marketData[i]["Low"] + marketData[i]["Close"]) / 4, 2)
            stochastic = getStochastic(len(marketData) - i - 1, IBClient.historicalDataArray)
            HAData.append({"Date" : marketData[i]["Date"] ,"HAOpen": ceil(haOpen * 100) / 100.0, "HAClose": ceil(haClose * 100) / 100.0, "Stochastic": stochastic})

            if DEBUG:
                print(str(i) + ". " + marketData[i]["Date"] + " HAOpen: " + str(haOpen) + " HAClose: " + str(haClose) + " Stochastic: " + str(getStochastic(len(marketData) - i - 1, IBClient.historicalDataArray)))
    except Exception as e:
        print("Exception in HA" + str(e))

    return HAData


def testHeikinAshi(IBClient):
    OverSold = 20
    OverBought = 80

    while not isinstance(IBClient.nextorderId, int):
        pass

    getCandles(IBClient, "50 D", "30 mins", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))

    while (IBClient.historicalDataEndStatus == False):
        pass

    heikinAshiData = calculateHeikinAshi(IBClient, IBClient.historicalDataArray, False)

    #for i in heikinAshiData:
    #    print(i)

    for i in range(4, len(heikinAshiData)):
        isTrade = False
        try:
            openCurrent = heikinAshiData[i]["HAOpen"]
            openOnePrevious = heikinAshiData[i - 1]["HAOpen"]
            closeCurrent = heikinAshiData[i]["HAClose"]
            closeOnePrevious = heikinAshiData[i - 1]["HAClose"]

            # Long Trade
            if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)):
                if ((heikinAshiData[i]["Stochastic"] > OverSold) and (
                        (heikinAshiData[i-1]["Stochastic"] < OverSold) or
                        (heikinAshiData[i-2]["Stochastic"] < OverSold) or
                        (heikinAshiData[i-3]["Stochastic"] < OverSold) or
                        (heikinAshiData[i-4]["Stochastic"] < OverSold))):
                    print(str(heikinAshiData[i]) + " -> Order: Long Trade")
                    isTrade = True

            # Short Trade
            if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)):
                if ((heikinAshiData[i]["Stochastic"] < OverBought) and (
                        (heikinAshiData[i-1]["Stochastic"] > OverBought) or
                        (heikinAshiData[i-2]["Stochastic"] > OverBought) or
                        (heikinAshiData[i-3]["Stochastic"] > OverBought) or
                        (heikinAshiData[i-4]["Stochastic"] > OverBought))):
                    print(str(heikinAshiData[i]) + " -> Order: Short Trade")
                    isTrade = True

            # No Trade
            if isTrade == False:
                print(str(heikinAshiData[i]) + " -> Order: No Trade")


        except Exception as e:
            print("bla")