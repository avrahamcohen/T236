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