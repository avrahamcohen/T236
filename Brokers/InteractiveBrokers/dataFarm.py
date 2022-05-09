#!/usr/bin/env python3

def getCandles(IBClient, timeResolution, barSize, whatToShow, contract):
    IBClient.reqHistoricalData(1, contract, "", timeResolution, barSize, whatToShow, 0, 1, False, [])

def calculateStochastic(candlePosition, marketData):
    stocasticData = []
    position = len(marketData) - 1

    for marketDataRecord in range(position - candlePosition, position - candlePosition - 12, -1):
        stocasticData.append(marketData[marketDataRecord])

    return (((stocasticData[0]["Close"] - findMin(stocasticData)) * 100) / (findMax(stocasticData) - findMin(stocasticData)))

def getStochastic(candlePosition, marketData):
    value = ((calculateStochastic(candlePosition, marketData) + calculateStochastic(candlePosition + 1, marketData) + calculateStochastic(candlePosition + 2, marketData)) / 3)
    return value

def getHeikinAshi(marketData, DEBUG=False, BACKTEST=False):
    haOpen = 0
    haClose = 0

    HAData = []

    try:
        for i in range(0, len(marketData) - 1):
            if i == 0:
                haOpen = round(marketData[i]["Open"], 2)
            else:
                haOpen = round((haOpen + haClose) / 2, 2)

            haClose = round(
                (marketData[i]["Open"] + marketData[i]["High"] + marketData[i]["Low"] + marketData[i]["Close"]) / 4, 2)

            '''For back testing purposes'''
            if BACKTEST:
                stochastic = getStochastic(len(marketData) - i - 1, marketData)
                HAData.append({"Date": marketData[i]["Date"], "HAOpen": haOpen, "HAClose": haClose, "Stochastic": stochastic})
                print(marketData[i]["Date"] + " HAOpen: " + str(haOpen) + " HAClose: " + str(haClose) + " Stochastic: " + str(stochastic))

            else:
                HAData.append({"HAOpen": haOpen, "HAClose": haClose})

            if DEBUG:
                print(marketData[i]["Date"] + " HAOpen: " + str(haOpen) + " HAClose: " + str(haClose))

    except Exception as e:
        print("Exception in HA" + str(e))

    return HAData

def findMax(values):
    numbers = []
    for value in values:
        numbers.append(value["High"])

    return max(numbers)

def findMin(values):
    numbers = []
    for value in values:
        numbers.append(value["Low"])

    return min(numbers)